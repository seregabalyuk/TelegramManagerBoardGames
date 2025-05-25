from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
#from src.database import Boardgame# BoardGame () .Boardgame

from database import TypeBoardgame, User
from handlers.States import States
from handlers import ask
from handlers import delete

router = Router()


def get_buttons_with_info(args) :
  return [
    [
      InlineKeyboardButton(text="добавить", callback_data="add " + args[1]),
      InlineKeyboardButton(text="попросить", callback_data=f"{args[0]} {args[1]} ask")
    ],
    [delete.button()]
  ]



@router.message(Command("search"))
async def catcher(message: types.Message, state: FSMContext):
  await state.update_data(command="search")
  await state.set_state(States.wrote_find_game)
  await message.answer("Напишите название настольной игры")


@router.callback_query(F.data.regexp(r"^search [-+]?\d+$"))
async def selected_callback(callback: types.CallbackQuery) :
  data = callback.data
  args = data.split()
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
  game_status = ""
  if not is_wish_list and count_c == 0:
    game_status = "у вас нет этой игры"
  elif not is_wish_list and count_c > 0:
    game_status = f"есть в количестве {count_c}"
  elif is_wish_list and count_c == 0:
    game_status = "есть в списке желаемых"
  elif is_wish_list and count_c > 0:
    game_status = "есть в списке желаемых и в своих в количестве {count_c}"


  buttons = get_buttons_with_info(args)
  buttons.insert(0, [InlineKeyboardButton(text="Посмотреть, у кого есть", callback_data=data + " co")])
  buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
  answer = f"""
Название: {game.name}
Количество игроков: {game.min_players}-{game.max_players}
Продолжительность игры: {game.playing_time()} мин.
Возраст: {game.age}+
статус: {game_status}
  """

  await callback.message.reply_photo(photo=game.image_url,caption=answer, reply_markup=buttons)
  await callback.message.delete()


@router.callback_query(F.data.regexp(r"^search [-+]?\d+ co$"))
async def after_show(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()

  user = User.load(callback.from_user.id)
  users_with_game = user.get_friends(with_game_id=int(args[1]))
  users_without_game = user.get_friends(with_game_id=int(args[1]), is_bought=False)
  if len(users_with_game) > 0:
    answer = "\n\nДрузья с этой игрой:\n"
    for obj in users_with_game:
      answer += f"{obj.user.name} из {obj.group.name}"
      if obj.game.took is None:
        answer += "(свободна)\n"
      else:
        answer += "(занята)\n"
  else:
    answer = "\n\nДрузей с этой игрой нет\n"

  if len(users_without_game) > 0:
    answer += "\nДрузья с этой игрой в списке желаний:\n"
    for obj in users_without_game:
      answer += f"{obj.user.name} из {obj.group.name}\n"
  else:
    answer += "\nДрузей с этой игрой в списке желаний нет\n"
  
  buttons = get_buttons_with_info(args)
  buttons = InlineKeyboardMarkup(inline_keyboard=buttons)

  await callback.message.edit_caption(
    caption=callback.message.caption + answer, 
    reply_markup=buttons
  )


@router.callback_query(F.data.regexp(r"^search [-+]?\d+ ask$"))
async def asked_game(callback: types.CallbackQuery) :
  data = callback.data
  args = data.split()

  user = User.load(callback.from_user.id)
  users_with_game = user.get_friends(with_game_id=int(args[1]))

  buttons = []
  for obj in users_with_game:
    if obj.game.took is None:
      print(obj.user.name)
      buttons.append([ask.button(obj.user, obj.game)])
  buttons.append([delete.button()])
  
  buttons = InlineKeyboardMarkup(inline_keyboard=buttons)

  await callback.message.edit_caption(
    caption="", 
    reply_markup=buttons
  )