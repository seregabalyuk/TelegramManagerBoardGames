from aiogram import Dispatcher, F, types
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from database import User, Boardgame

router = Router()

@router.callback_query(F.data == "delete")
async def handle_callback(callback: types.CallbackQuery):
  await callback.message.delete()



@router.callback_query(F.data.regexp(r"^delete game [+-]?\d+$"))
async def view_friends(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()
  try:
    game = Boardgame.load_by_id(int(args[2]))
  except:
    await callback.message.answer("Уже удалён")
  else:
    from_user = User.load(callback.from_user.id)
    place = "своих" if game.is_bought else "вишлиста"
    answer = f"вы хотите удалить '{game.name}' из {place}"
    buttons = [[
      InlineKeyboardButton(text=f"да", callback_data=f"delete s game {args[2]}"),
      InlineKeyboardButton(text=f"нет", callback_data=f"delete")
    ]]
    buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(answer, reply_markup=buttons)


@router.callback_query(F.data.regexp(r"^delete s game [+-]?\d+$"))
async def view_friends(callback: types.CallbackQuery):
  data = callback.data
  args = data.split()
  try:
    game = Boardgame.load_by_id(int(args[3]))
  except:
    answer = "Уже удалён"
  else:
    try:
      from_user = User.load(callback.from_user.id)
      place = "своих" if game.is_bought else "вишлиста"
      answer = f"удалил '{game.name}' из {place}"
      game.delete()
    except Exception as error:
      print("Error in file src/handlers/delete.py:")
      print(error)
      answer = "Ошибка в базе данных"
  await callback.message.edit_text(answer)


def button():
  return InlineKeyboardButton(text="Закрыть", callback_data="delete")