from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.States import States
from database import GameBoard

router = Router()


def create_buttons(boardgames):
  buttons = []
  for (id, name) in boardgames:
    buttons.append([InlineKeyboardButton(text=name, callback_data=f"{id}")])
  buttons.append([InlineKeyboardButton(text="нет нужной игры", callback_data=f"not found")])
  return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(States.wrote_find_text)
async def give_chosen(message: types.Message, state: FSMContext):
  boardgame_name = message.text
  boardgames = GameBoard.find(boardgame_name)
  data = await state.get_data()
  if len(boardgames) == 0:
    await state.clear()
    await state.set_state(None)
    await message.answer(f"Я не нашёл {boardgame_name}. Попробуйте еще раз /{command}")
  else:
    buttons = create_buttons(boardgames)
    if data["command"] == "add":
      await state.set_state(States.found_add_game)
    elif data["command"] == "search":
      await state.set_state(States.found_search_game)
    else:
      print("your not give type function in find.py")
    await message.answer(f"Вот игры, которые я нашёл:", reply_markup=buttons)