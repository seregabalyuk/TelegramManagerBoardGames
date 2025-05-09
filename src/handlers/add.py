from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import GameBoard, User

router = Router()

class Add(StatesGroup):
  started = State()
  finded = State()
  selected = State()



@router.message(Command("add"))
async def add_step1(message: types.Message, state: FSMContext):
  await state.set_state(Add.started)
  await message.answer("Напишите название настольной игры")


def create_buttons(boardgames):
  buttons = []
  for (id, name) in boardgames:
    buttons.append([InlineKeyboardButton(text=name, callback_data=f"{id} {name}")])
  buttons.append([InlineKeyboardButton(text="нет нужной игры", callback_data=f"not found")])
  return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Add.started)
async def add_step2(message: types.Message, state: FSMContext):
  boardgame_name = message.text
  boardgames = GameBoard.find(boardgame_name)
  if len(boardgames) == 0:
    await state.clear()
    await message.answer(f"Я не нашёл {boardgame_name}. Попробуйте еще раз /add")
  else:
    buttons = create_buttons(boardgames)
    await state.set_state(Add.finded)
    await message.answer(f"Вот игры, которые я нашёл:", reply_markup=buttons)


@router.callback_query(StateFilter(Add.finded))
async def add_step3(callback: types.CallbackQuery, state: FSMContext):
  data = callback.data
  if data == "not found":
    await state.clear()
    await callback.message.edit_text("""
    Для повторной попытки поиска нажмите /add\nМожете ввести лишь часть названия.
    """)
  else:
    args = data.split()
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
    await state.set_state(Add.selected)
    await callback.message.edit_text(f"""Добавить {args[1]} в:""", reply_markup=buttons)
    # await callback.answer(f"вы выбрали настольную игру с id = {id}")


@router.callback_query(StateFilter(Add.selected))
async def add_step3(callback: types.CallbackQuery, state: FSMContext):
  data = callback.data
  if data == "closed":
    await state.clear()
    await callback.message.edit_text("""
    Можете попробовать ещё раз /add
    """)
  else:
    args = data.split()
    place = "свою коллекцию" if args[2] == "collection" else "вишлист"
    user = User.get(callback.from_user.id, callback.from_user.username)
    if user.add_boardgame(int(args[0]), args[2] == "collection"):
      await callback.message.edit_text(f"""Вы успешно добавили {args[1]} в {place}""")
    else:
      await callback.message.edit_text(f"""Я не смог добавить {args[1]} в {place}. Ошибка в базе данных.""")

  
  
  
