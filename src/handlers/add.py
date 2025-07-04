from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import GameBoard, User
from handlers.States import States

router = Router()


@router.message(Command("add"))
async def catcher(message: types.Message, state: FSMContext):
  await state.update_data(command="add")
  await state.set_state(States.wrote_find_text)
  await message.answer("Напишите название настольной игры")


@router.callback_query(StateFilter(States.found_add_game))
async def choose_place(callback: types.CallbackQuery, state: FSMContext):
  data = callback.data
  if data == "not found":
    await state.clear()
    await state.set_state(None)
    await callback.message.edit_text("""
    Для повторной попытки поиска нажмите /add\nМожете ввести лишь часть названия.
    """)
  else:
    args = data.split()
    user = User.get(callback.from_user.id, callback.from_user.username)
    game = GameBoard.load(int(args[0]))
    buttons = InlineKeyboardMarkup(
      inline_keyboard=[
        [
          InlineKeyboardButton(text="свои", callback_data=data + f" collection"),
          InlineKeyboardButton(text="вишлист", callback_data=data + f" wishlist")
        ],
        [
          InlineKeyboardButton(text="не добавлять", callback_data=f"closed")
        ]
      ]
    )
    await state.set_state(States.chose_place_add)
    await callback.message.edit_text(f"""Добавить {game.name} в:""", reply_markup=buttons)


@router.callback_query(StateFilter(States.chose_place_add))
async def finish(callback: types.CallbackQuery, state: FSMContext):
  data = callback.data
  if data == "closed":
    await callback.message.edit_text("""
    Можете попробовать ещё раз /add
    """)
  else:
    args = data.split()
    place = "свою коллекцию" if args[1] == "collection" else "вишлист"
    user = User.get(callback.from_user.id, callback.from_user.username)
    game = GameBoard.load(int(args[0]))
    if user.add_boardgame(int(args[0]), args[1] == "collection"):
      await callback.message.edit_text(f"""Вы успешно добавили {game.name} в {place}""")
    else:
      await callback.message.edit_text(f"""Я не смог добавить {game.name} в {place}. Ошибка в базе данных.""")
  await state.clear()
  await state.set_state(None)

