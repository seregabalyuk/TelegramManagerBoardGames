from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
import asyncio

import bot_loader as bl
from database import User, Boardgame
from handlers import delete

router = Router()

def button(user_to: User, game):
  if game.name == None:
    text = f"Попросить у {user_to.name}"
  else:
    text = f"Попросить {game.name} у {user_to.name}"
  return InlineKeyboardButton(
    text=text, 
    callback_data=f"ask {game.id} {user_to.id}"
  )


@router.callback_query(F.data.regexp(r"ask [-+]?\d+ [-+]?\d+"))
async def ask(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()
  
  game = Boardgame.load_by_id(int(args[1]))
  to_user = User.load_by_id(int(args[2]))
  from_user = User.load(callback.from_user.id)

  buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(
        text="дать", 
        callback_data=f"ask g {game.id} {from_user.id}"
      ),
      InlineKeyboardButton(
        text="отказаться",
        callback_data=f"ask ng {game.id} {from_user.id}"
      )
    ],
    [delete.button()]
  ])
  
  
  key = StorageKey(chat_id=to_user.telegram_id, user_id=to_user.telegram_id, bot_id=bl.bot.id)
  await bl.bot.send_message(
    chat_id = to_user.telegram_id,
    text = f"У тебя попросил {game.name} пользователь с именем {from_user.name}",
    reply_markup=buttons
  )
  return True


@router.callback_query(F.data.regexp(r"ask n?g [-+]?\d+ [-+]?\d+"))
async def ask(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()

  game = Boardgame.load_by_id(int(args[2]))
  to_user = User.load(callback.from_user.id)
  from_user = User.load_by_id(int(args[3]))
  is_give = False

  if args[1] == "ng":
    await callback.message.edit_text(f"""Ответ принят""")
  elif args[1] == "g":
    try:
      if to_user.give_game(game.id, from_user):
        await callback.message.edit_text(f"""Вы дали игру {game.name} пользователю {from_user.name}""")
        is_give = True
      else:
        await callback.message.edit_text(f"""Вы уже дали кому-то игру {game.name}""")
    except Exception as error:
      print(error)
      await callback.message.edit_text(f"""ошибка в базе данных""")
  if is_give:
    await bl.bot.send_message(
      chat_id = from_user.telegram_id,
      text = f"{to_user.name} дал тебе {game.name}"
    )
  else:
    await bl.bot.send_message(
      chat_id = from_user.telegram_id,
      text = f"{to_user.name} не смог дать тебе {game.name}"
    )
