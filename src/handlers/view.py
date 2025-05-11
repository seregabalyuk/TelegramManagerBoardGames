from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User, Group
from handlers.States import States

router = Router()

def create_buttons(gameboards):
  answer = []
  for (id, name, ouner) in gameboards:
    answer.append([
      InlineKeyboardButton(
        text=f"попросить {name} у {ouner}", 
        callback_data=f"{id} {name} {ouner}"
      )
    ])
  answer.append([
    InlineKeyboardButton(
      text=f"Закрыть", 
      callback_data=f"close"
    )
  ])
  return InlineKeyboardMarkup(inline_keyboard=answer)


@router.message(Command("view"))
async def catcher(message: types.Message, state: FSMContext):
  await state.set_state(States.open_view_games)
  chat_type = message.chat.type
  if chat_type in ["group", "supergroup"]:
    group = Group.load_without_password(message.chat.id)
    gameboards = group.all_gameboards()
    buttons = create_buttons(gameboards)
    await message.answer(text="Все свободные настольные игры в вашей группе:", reply_markup=buttons)


@router.callback_query(StateFilter(States.open_view_games))
async def button_touch(callback: types.CallbackQuery, state: FSMContext):
  data = callback.data
  user = User.load(callback.from_user.id)
  if data == "close":
    await state.clear()
    await state.set_state(None)
    await callback.message.edit_text(f"""
    {user.name} закрыл список игр.
    """)
  else:
    args = data.split()
    await callback.message.answer(f"""{user.name} попросил {args[1]} у {args[2]}""")


