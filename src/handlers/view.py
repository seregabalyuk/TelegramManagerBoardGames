from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State

from database import User, Group, Boardgame
from handlers.States import States
from handlers import ask
from handlers import delete

router = Router()

def create_buttons(gameboards):
  answer = []
  for (game, ouner) in gameboards:
    answer.append([ask.button(ouner, game)])
  answer.append([delete.button()])
  return InlineKeyboardMarkup(inline_keyboard=answer)


@router.message(Command("view"))
async def catcher(message: types.Message):
  chat_type = message.chat.type
  if chat_type in ["group", "supergroup"]:
    group = Group.load_without_password(message.chat.id)
    gameboards = group.all_gameboards()
    buttons = create_buttons(gameboards)
    await message.answer(text="Все свободные настольные игры в вашей группе:", reply_markup=buttons)
  else :
    buttons = [
      [
        InlineKeyboardButton(text="друзей", callback_data="view f"), 
      ],
      [
        InlineKeyboardButton(text="своих игр", callback_data="view myg"),
        InlineKeyboardButton(text="свой вишлист", callback_data="view myw")
      ],
      [
        InlineKeyboardButton(text="своих групп с ботом", callback_data="view gr")
      ],
      [InlineKeyboardButton(text="вишлист друга", callback_data="view wf")],
      [delete.button()]
    ]
    buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
    answer = """Для того что бы посмотреть игры в группе, напишиете /view там.\nТут вы может посмотерть список:"""
    await message.answer(answer, reply_markup=buttons)


@router.callback_query(F.data.regexp(r"^view f$"))
async def view_friends(callback: types.CallbackQuery):
  from_user = User.load(callback.from_user.id)
  answer = "Ваши друзья: "
  friends = from_user.get_friends()
  for obj in friends:
    answer += "\n" + obj.user.name + " в группе " + obj.group.name
  await callback.message.edit_text(answer)



@router.callback_query(F.data.regexp(r"^view myg$"))
async def view_friends(callback: types.CallbackQuery):
  from_user = User.load(callback.from_user.id)
  answer = "Ваши игры: "
  games = from_user.get_games()
  for row in games :
    if row[1] is None :
      answer += "\n" + row[0] + " (свободна)"
    else :
      answer += "\n" + row[0] + " y " + User.load_by_id(row[1]).name
  await callback.message.edit_text(answer)


@router.callback_query(F.data.regexp(r"^view myw$"))
async def view_friends(callback: types.CallbackQuery):
  from_user = User.load(callback.from_user.id)
  answer = "Ваш вишлист: "
  games = from_user.get_games(is_bought = False)
  buttons = []
  for row in games:
    buttons.append([
      InlineKeyboardButton(text=f"{row[0]}, удалить 🗑️?", callback_data=f"delete game {row[3]}")
    ])
  buttons.append([delete.button()])
  buttons = InlineKeyboardMarkup(inline_keyboard=buttons)  
  await callback.message.edit_text(answer, reply_markup=buttons)


@router.callback_query(F.data.regexp(r"^view gr$"))
async def view_friends(callback: types.CallbackQuery):
  from_user = User.load(callback.from_user.id)
  answer = "Ваши группы: "
  groups = from_user.get_groups()
  for row in groups :
    answer += "\n" + row[1]
  await callback.message.edit_text(answer)


@router.callback_query(F.data.regexp(r"^view wf$"))
async def view_friends(callback: types.CallbackQuery,  state: FSMContext):
  answer = "Введите ник друга:"
  await state.set_state(States.wrote_find_user)
  await callback.message.edit_text(answer)



@router.message(States.wrote_find_user)
async def view_friends(message: types.Message, state: FSMContext):
  username = message.text
  user = User.load_by_name(username)
  answer = ""
  if user is None:
    answer = f"Пользователь с ником {username} не найден"
  else:
    games = user.get_games(is_bought = False)
    if len(games) == 0:
      answer = f"Вишлист {user.name} пустой"
    else:
      answer = f"Вишлист {user.name}:"
      for row in games :
        answer += "\n" + row[0]
    

  await state.clear()
  await state.set_state(None)
  await message.answer(answer)


