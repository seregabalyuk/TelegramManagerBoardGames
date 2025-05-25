from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.States import States
from database import TypeBoardgame
from handlers import delete

router = Router()


def create_buttons(boardgames, callfunc):
  buttons = []
  for (id, name) in boardgames:
    buttons.append([InlineKeyboardButton(text=name, callback_data=f"{callfunc} {id}")])
  buttons.append([delete.button()])
  return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(States.wrote_find_game)
async def give_chosen(message: types.Message, state: FSMContext):
  boardgame_name = message.text
  boardgames = TypeBoardgame.find(boardgame_name)
  data = await state.get_data()

  if len(boardgames) == 0:
    await state.clear()
    await state.set_state(None)
    await message.answer(f"Я не нашёл {boardgame_name}. Попробуйте еще раз /{data["command"]}")
  elif len(boardgames) > 100:
    await state.clear()
    await state.set_state(None)
    await message.answer(f"Игр с словом {boardgame_name} слишком много . Попробуйте более точно написать /{data["command"]}")
  else:
    buttons = create_buttons(boardgames, data["command"])
    await state.clear()
    await state.set_state(None)
    await message.answer(f"Вот игры, которые я нашёл:", reply_markup=buttons)