import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, JOIN_TRANSITION
#from aiofram.types
from psycopg2 import Error

def get_connect() :
    return psycopg2.connect(dbname="board_game_database", user="board_game_bot", password="bot", port="5432", host="localhost")
async def register(user: types.user) :
    connect = get_connect()
    try :
        connect.cursor().execute("INSERT INTO users (telegram_id, username) VALUES (%s, %s)", (str(user.id), str(user.username)))
        connect.commit()
        return "You are registred"
    except Error as e :
        return "bruh, " + str(e.pgerror)
    finally :
        connect.close()

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



@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))#.add_bot IS_NOT_MEMBER >> IS_MEMBER
async def bot_added_as_member(event: types.ChatMemberUpdated) : #.
    connect = get_connect()
    try : #trey
        chat = event.chat#chat
        connect.cursor().execute("INSERT INTO group_users (telegram_group_id, name) VALUES (%s, %s);", (str(chat.id), str(chat.title)))#teke
        connect.commit()
        await event.answer("group registerd")#00
    except Error as e :
        await event.answer("bruh, group")#awq#e.#.
    kb = [[types.KeyboardButton(text="join"), types.KeyboardButton(text="deny")]]#
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)#
    await event.answer("do you want to join" + str(event.chat.title), reply_markup=keyboard)## .id .username
    #print('bruh')#await

@dp.message(F.text == "join")
async def join_to_group(message: types.Message) :
    answer = await register(message.from_user)
    await message.answer(str(answer), reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text == "deny")
async def deny(message: types.Message) : #eeeeeeeeee
    await message.answer("((", reply_markup=types.ReplyKeyboardRemove())#.u.u.u.u.u.u.u





# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, allowed_updates=["message", "chat_member", "inline_query", "my_chat_member"])

if __name__ == "__main__":
    asyncio.run(main())
