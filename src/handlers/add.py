from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import TypeBoardgame, User
from handlers.States import States
from handlers import delete

router = Router()


@router.message(Command("add"))
async def catcher(message: types.Message, state: FSMContext):
  await state.update_data(command="add")
  await state.set_state(States.wrote_find_game)
  await message.answer("Напишите название настольной игры")


@router.callback_query(F.data.regexp(r"^add [-+]?\d+$"))
async def choose_place(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()
  user = User.get(callback.from_user.id, callback.from_user.username)
  game = TypeBoardgame.load_by_id(int(args[1]))

  game_info = User.load(callback.from_user.id).check_game(game.id)
  game_status = ""
  count_c = 0
  is_wish_list = False
  for info in game_info:
    if info[1]:
      count_c += 1
    else:
      is_wish_list = True
  
  if not is_wish_list and count_c == 0:
    game_status = "Добавить"
  elif not is_wish_list and count_c > 0:
    game_status = f"Уже у вас есть в количестве {count_c}.\nВсе равно добавить "
  elif is_wish_list and count_c == 0:
    game_status = "Есть в списке желаемых.\nДобавить "
  elif is_wish_list and count_c > 0:
    game_status = "Есть в списке желаемых и в своих в количестве {count_c}.\nВсе равно добавить "
  
  buttons = InlineKeyboardMarkup(
    inline_keyboard=[
      [
        InlineKeyboardButton(text="свои", callback_data=data + f" c"),
        InlineKeyboardButton(text="вишлист", callback_data=data + f" w")
      ] if not is_wish_list else [
        InlineKeyboardButton(text="свои", callback_data=data + f" c")
      ],
      [
        delete.button()
      ]
    ]
  )
  answer = f"""{game_status} "{game.name}" в: """
  await callback.message.reply_photo(photo=game.image_url,caption=answer, reply_markup=buttons)
  await callback.message.delete()


@router.callback_query(F.data.regexp(r"^add [-+]?\d+ [wc]$"))
async def finish(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()
  place = "свою коллекцию" if args[2] == "c" else "свой вишлист"
  user = User.get(callback.from_user.id, callback.from_user.username)
  game = TypeBoardgame.load_by_id(int(args[1]))
  if user.add_boardgame(int(args[1]), args[1] == "c"):
    await callback.message.answer(f"""Вы успешно добавили {game.name} в {place}""")
  else:
    await callback.message.answer(f"""Я не смог добавить {game.name} в {place}. Ошибка в базе данных.""")
  await callback.message.delete()

