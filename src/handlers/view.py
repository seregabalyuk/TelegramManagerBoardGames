from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User, Group
from handlers.States import States
from handlers import ask

router = Router()

def create_buttons(gameboards):
  answer = []
  for (id, name, ouner) in gameboards:
    answer.append([
      InlineKeyboardButton(
        text=f"попросить {name} у {ouner.name}", 
        callback_data=f"{id} {name} {ouner.id} {ouner.telegram_id} {ouner.name}"
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
  from_user = User.load(callback.from_user.id)
  if data == "close":
    await state.clear()
    await state.set_state(None)
    await callback.message.edit_text(f"""
    {from_user.name} закрыл список игр.
    """)
  else:
    args = data.split()
    to_user = User.User(int(args[2]), int(args[3]), args[4])
    game_id = int(args[0])
    game_name = args[1]
    await ask.ask(from_user, to_user, game_id, game_name)
    await callback.message.answer(f"""{from_user.name} попросил {game_name} у {to_user.name}""")


