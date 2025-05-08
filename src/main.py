from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import asyncio

from handlers import start, groups


token = open('src/token.txt').read().strip()
bot = Bot(token=token)
dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(groups.router)

async def main():
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())

