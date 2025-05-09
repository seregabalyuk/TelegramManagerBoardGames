from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from handlers import start, groups, add, search_game


token = open('token.txt').read().strip()#src/
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(storage=storage)
dp.include_router(start.router)
dp.include_router(groups.router)
dp.include_router(add.router)
dp.include_router(search_game.router)



async def set_bot_commands(bot: Bot):
  commands = [
    BotCommand(command="/start", description="Запуск бота"),
    BotCommand(command="/add", description="Добавить настольную игру"),
    BotCommand(command="/search", description="game search"),
  ]
  await bot.set_my_commands(commands)


async def main():
  await set_bot_commands(bot)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())

