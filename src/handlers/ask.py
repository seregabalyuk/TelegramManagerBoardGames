from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
import asyncio

import bot_loader as bl
from handlers.States import States
from database import User, GameBoard


router = Router()

async def ask(from_user, to_user, game_id, game_name):
  buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(
        text="дать", 
        callback_data=f"give {from_user.id} {game_id}"
      ),
      InlineKeyboardButton(
        text="отказаться",
        callback_data=f"not_give {from_user.id} {game_id}"
      )
    ]
  ])
  
  key = StorageKey(chat_id=to_user.telegram_id, user_id=to_user.telegram_id, bot_id=bl.bot.id)
  await bl.dp.storage.set_state(key, States.get_answer_ask)
  # state = FSMContext(bl.dp.storage, to_user.telegram_id, to_user.telegram_id)
  # await state.set_state(States.get_answer_ask)
  await bl.bot.send_message(
    chat_id = to_user.telegram_id,
    text = f"У тебя попросил {game_name} пользователь с именем {from_user.name}",
    reply_markup=buttons
  )


@router.callback_query(StateFilter(States.get_answer_ask))
async def get_answer(callback: types.CallbackQuery, state: FSMContext):
  args = callback.data.split()
  if len(args) != 3:
    print("not corret work button in ask")
    return
  from_user = User.load_by_id(int(args[1]))
  to_user = User.load(callback.from_user.id)
  game_name = GameBoard.load_name_by_id(int(args[2]))
  if args[0] == "not_give":
    await state.clear()
    await state.set_state(None)
    await callback.message.edit_text(f"""Ответ принят""")
  elif args[0] == "give":
    await state.clear()
    await state.set_state(None)
    await callback.message.edit_text(f"""Вы дали игру {game_name} пользователю {from_user.name}""")
  