import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, JOIN_TRANSITION
#from aiofram.types
from psycopg2 import Error, sql

ERROR_MSG = "bruh, "
def get_connect() :
    return psycopg2.connect(dbname="board_game_database", user="board_game_bot", password="bot", port="5432", host="localhost")


class UsersRel(object) : #сдфыы  users_rel  usersRel  UsrersRel

    def __init__(self, idd, telegram_id, username) :
        self.id = idd
        self.telegram_id = telegram_id
        self.username = username

    def insert(self, telegram_id, username):# insi
        coonect = get_connect()
        #answer
        try :# cetch
            coonect.cursor().execute("INSERT INTO users (telegram_id, username) VALUES (%s, %s)", (str(telegram_id), str(username)))
            coonect.commit()#.v
            return "ok"# "in"
        except Error as e :
            return str(e.pgerror)#.

    def select(self, username=None, telegram_id=None): #
        connect = get_connect()#connact , telegram_id
        query = "SELECT * FROM users WHERE" # EHERE
        param = ()#,
        cursor = connect.cursor()
        if username is None and telegram_id is not None : # Nane
            query = query + " telegram_id = %s"#connect.cursor().execute("SELECT (users_id) FROM users WHERE telegram_id = %s")# EHERE
            param = (str(telegram_id), )
        if username is not None and telegram_id is None : # telegtam_id
            query = query + "username = %s"#connect.cursor()
            param = (str(username), )
        cursor.execute(query, param)
        result = cursor.fetchone()
        return UsersRel(result[0], result[1], result[2])
    staticmethod(insert)#inde indert eer3rre
    staticmethod(select)

async def register(user: types.user) :
    connect = get_connect()
    try :
        connect.cursor().execute("INSERT INTO users (telegram_id, username) VALUES (%s, %s);", (str(user.id), str(user.username)))
        connect.commit()
        return "You are registred"
    except Error as e :
        return ERROR_MSG + str(e.pgerror)
    finally :
        connect.close()

async def join_to_grouph(user: types.user, chat_id: int) :
#\
    connect = get_connect()
    cursor = connect.cursor()
    cursor.execute("SELECT users_id FROM users WHERE telegram_id = %s", (str(user.id), ))
    user_row = cursor.fetchone()#[0] id_row ..
    cursor.execute("SELECT group_id FROM group_users WHERE telegram_group_id = %s", (str(chat_id), ))
    group_row = cursor.fetchone()
    if not (user_row is None or group_row is None) :
        try :
            cursor.execute("INSERT INTO group_member (group_id, users_id) VALUES (%s, %s)", (group_row[0], user_row[0]));#
            connect.commit()
            return "added to group"
        except Error as e :
            return ERROR_MSG + str(e.pgerror)
    else :
        return ERROR_MSG + "group is " + str(group_row) + ", user is " + str(user_row)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.DEBUG)#.INFO .ERROR
# Объект бота
token = open('token.txt').read().strip()
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()


router = Router()
dp.include_router(router)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!, Что дальше?")


@dp.message(Command("register"))
async def cmd_register(message: types.Message) :
    answer = await register(message.from_user)
    await message.answer(str(answer))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added_as_member(event: types.ChatMemberUpdated) :
    connect = get_connect()
    #UsersRel.insert()
    try :
        chat = event.chat
        connect.cursor().execute("INSERT INTO group_users (telegram_group_id, name) VALUES (%s, %s);", (str(chat.id), str(chat.title)))#teke
        connect.commit()
        await event.answer("group registerd")
    except Error as e:
        await event.answer(ERROR_MSG + "group")
    kb = [[types.KeyboardButton(text="join"), types.KeyboardButton(text="deny")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await event.answer("do you want to join" + str(event.chat.title), reply_markup=keyboard)


@dp.message(F.text == "join")
async def join_to_group(message: types.Message) :
    answer = await register(message.from_user)
    jg = await join_to_grouph(message.from_user, chat_id = message.chat.id)
    await message.answer(str(answer) + str(jg), reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == "deny")
async def deny(message: types.Message) :
    await message.answer("((", reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command("lookup"))
async def cmd_exists(message: types.Message, command: CommandObject) :
    answer = ERROR_MSG
    if command.args is None :
        answer = "what should lookup?"
    else :
        connect = get_connect()
        cursor = connect.cursor()
        query = sql.SQL("SELECT games_name FROM games WHERE games_name LIKE {pattern};").format(pattern=sql.Literal(("%" + str(command.args)) + "%"))
        cursor.execute(query)
        print("%" + str(command.args) + "%")
        answer = str(cursor.fetchall())
        connect.close()
    await message.answer(answer)


@dp.message(Command("addgame"))
async def cmd_addgame(message: types.Message, command: CommandObject) :
    answer = ERROR_MSG

    if command.args is None :
        answer = "game is not specified"
    else :
        connect = get_connect()
        cursor = connect.cursor()
        cursor.execute("SELECT users_id FROM users WHERE telegram_id = %s", (str(message.from_user.id), ))
        id_row = cursor.fetchone()
        cursor.execute("SELECT games_id FROM games WHERE games_name = %s", (str(command.args), ))
        game_row = cursor.fetchone()
        if not (id_row is None or game_row is None) :
            try :
                cursor.execute("INSERT INTO gameboards (users_id, games_id, if_bought, if_free, owner_user_id) VALUES (%s, %s, true, true, %s)", (str(id_row[0]), str(game_row[0]), str(id_row[0])))
                connect.commit();
                answer = "game added"
            except Error as e :
                answer = ERROR_MSG + e.pgerror

        else :
            answer = ERROR_MSG + "user_id is " + str(id_row) + " game_id is " + str(game_row)
    await message.answer(answer)


@dp.message(Command("lease"))
async def cmd_lease(message: types.Message, command: CommandObject) :
    answer = ""
    if command.args is None :
        answer = "no game, no user..."
    else :
        args = str(command.args).split()
        if len(args) != 2 :
            answer = "not enough or too much arguments"
        else :
            connect = get_connect()
            cursor = connect.cursor()
            cursor.execute("SELECT (games_id) FROM games WHERE games_name = %s", (args[0], ))
            game_row = cursor.fetchone()
            cursor.execute("SELECT (users_id) FROM users WHERE telegram_id = %s", (str(message.from_user.id), ))#*
            fromuser_row = cursor.fetchone()
            cursor.execute("SELECT (users_id) FROM users WHERE username = %s", (args[1], ))
            touser_row = cursor.fetchone()
            if (game_row is None or fromuser_row is None or touser_row is None) :
                answer = ERROR_MSG + "game is " + str(game_row) + ", owner is " + str(fromuser_row) + ", target user is " + str(touser_row)
            else :

                cursor.execute("SELECT (owner_user_id) FROM gameboards WHERE users_id = %s AND games_id = %s", (str(fromuser_row[0]), str(game_row[0])))
                current_owner = cursor.fetchone()
                if current_owner is None :
                    answer = str(game_row[0]) +  " isnt " + str(fromuser_row[0]) + "'s game  found"
                else :
                    if current_owner[0] == fromuser_row:
                        try :
                            cursor.execute("UPDATE gameboards SET owner_user_id = %s WHERE users_id = %s AND games_id = %s",
                                        (str(touser_row[0]), str(fromuser_row[0]), str(game_row[0])))
                            connect.commit()
                            answer = "game leased"
                        except Error as e :
                            answer = ERROR_MSG + str(e.pgerror)
                    else :
                        answer = ERROR_MSG + "according to database game is leased"
    await message.answer(answer)


@dp.message(Command("return"))
async def cmd_return(message: types.Message, command: CommandObject) :
    answer = ""
    if command.args is None :
        answer = "what should be returned????"
    else :
        connect = get_connect()
        cursor = connect.cursor()
        cursor.execute("SELECT users_id FROM users WHERE telegram_id = %s;", (str(message.from_user.id), ))
        user_row = cursor.fetchone()
        cursor.execute("SELECT games_id FROM games WHERE games_name = %s;", (command.args, ))
        game_row = cursor.fetchone()
        if user_row is None or game_row is None :
            answer = ERROR_MSG + "user is " + str(user_row) + ", game is " + ";" + str(game_row)
        else :
            cursor.execute("SELECT * FROM gameboards WHERE games_id = %s AND owner_user_id = %s;", (str(game_row[0]), str(user_row[0])))
            if cursor.fetchone() is None :
                answer = "looks like you had not leased this game"
            else :
                try :
                    cursor.execute("UPDATE gameboards SET owner_user_id = users_id WHERE games_id = %s AND owner_user_id = %s;", (str(game_row[0]), str(user_row[0])))
                    connect.commit()
                    answer = "game successfully returned;"
                except Error as e :
                    answer = ERROR_MSG + e.pgerror
    await message.answer(answer)







# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, allowed_updates=["message", "chat_member", "inline_query", "my_chat_member"])

if __name__ == "__main__":
    asyncio.run(main())
