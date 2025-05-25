from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User, Boardgame
from handlers import delete

router =  Router()


@router.message(Command("return"))
async def show_leased(message: types.Message) :
  leased_games = User.load(message.from_user.id).get_leased_games()
  buttons = []
  answer = ""
  if len(leased_games) == 0 :
    answer = "Похоже, Вы ничего ни у кого не брали"
  else :
    answer = "Вернуть: "
    for row in leased_games :
      buttons.append([
        InlineKeyboardButton(
          text=row[2] + " вернуть " + row[0], 
          callback_data="ret " + str(row[-1])
        )
      ])
  buttons.append([delete.button()])
  buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
  await message.answer(answer, reply_markup=buttons)


@router.callback_query(F.data.regexp(r"^ret [-+]?\d+$"))
async def return_chosen(callback: types.CallbackQuery) :
  data = callback.data
  args = data.split()
  message = callback.message
  answer = ""
  if data == "close" :
      await state.clear()
      await state.set_state(None)
      await message.delete()
      return
  if Boardgame.return_game(int(args[1])) :
      answer = "Игра успешно возвращена"
  else :
      answer = "Мы не смогли вернуть игру"
  await message.edit_text(answer)
