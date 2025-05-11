from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from handlers import (
  start, 
  groups, 
  add, 
  search,
  find,
  view,
  return_game
)
#import token_loader


token = open('token.txt').read().strip()#token_loader.load() src/
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(storage=storage)
dp.include_router(start.router)
dp.include_router(groups.router)
dp.include_router(add.router)
dp.include_router(search.router)
dp.include_router(find.router)
dp.include_router(view.router)
dp.include_router(return_game.router)


async def set_bot_commands(bot: Bot):
  commands = [
    BotCommand(command="/start", description="Запуск бота"),
    BotCommand(command="/add", description="Добавить настольную игру"),
    BotCommand(command="/search", description="Найти игру"),
    BotCommand(command="/view", description="Посмотреть игры"),
    BotCommand(command="/return", description="Вернуть игру другу")
  ]
  await bot.set_my_commands(commands)
