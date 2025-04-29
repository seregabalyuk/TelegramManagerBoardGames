import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER#[a s
#from aiofram.types
from psycopg2 import Error

def get_connect() :
    return psycopg2.connect(dbname="board_game_database", user="board_game_bot", password="bot", port="5432", host="localhost")

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
token = open('token.txt').read().strip()
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()

router = Router()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!, Что дальше?")

@dp.message(Command("register"))
async def cmd_register(message: types.Message) :
    connect = get_connect()
    cursir = connect.cursor()
    #cursir.execute("SELECT version();")#.executr()##
    user = message.from_user
    #user.
    #message.chat.
    bot.get_chat()  #.user#.get_us
    #№user.cha
    message.chat
    #user.id.
    try :
        cursir.execute("INSERT INTO users (telegram_id, username) VALUES (%s, %s);", (str(user.id), str(user.username)))#WW $# int() % 1000
        connect.commit()
        await message.answer("done!" + str(int(message.from_user.id)))  # cursor  str(cursir.fetchone()) .username
    except Error as e :
        await message.answer("Already registred!")

@router.add_bot(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))#
async def bot_added(event: types.ChatMemberUpdated) : #.
    kb = [types.KeyboardButton(text="join"), types.KeyboardButton(text="deny")]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await event.answer("do you want to join", reply_markup=keyboard)

@dp.message(F.text == "join")
async def join_to_group(message: types.Message) :
    await message.reply("you have been joined", reply_markup=types.ReplyKeyboardRemove())#'' .KeyBel ehe




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())