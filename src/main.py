from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
import asyncio

from handlers import start, groups


token = open('src/token.txt').read().strip()
bot = Bot(token=token)
dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(groups.router)


async def set_bot_commands(bot: Bot):
  commands = [
    BotCommand(command="/start", description="Запуск бота"),
    BotCommand(command="/add", description="Добавить настольную игру"),
  ]
  await bot.set_my_commands(commands)


async def main():
  await set_bot_commands(bot)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())

