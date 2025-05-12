from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

from database import User, GameBoard
from handlers.States import States


router =  Router()


@router.message(Command("return"))
async def show_leased(message: types.Message, state: FSMContext) :
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
                callback_data=str(row[-1])
              )
            ])
    buttons.append([
      InlineKeyboardButton(
        text="закрыть", 
        callback_data="close"
      )
    ])
    buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
    await state.set_state(States.leased_shown)
    await message.answer(answer, reply_markup=buttons)


@router.callback_query(StateFilter(States.leased_shown))
async def return_chosen(callback: types.CallbackQuery, state: FSMContext) :
    data = callback.data
    message = callback.message
    answer = ""
    if data == "close" :
        await state.clear()
        await state.set_state(None)
        await message.delete()
        return
    if GameBoard.return_game(int(data)) :
        answer = "Игра успешно возвращена"
    else :
        answer = "Мы не смогли вернуть игру"
    await state.clear()
    await state.set_state(None)
    await message.edit_text(answer)
