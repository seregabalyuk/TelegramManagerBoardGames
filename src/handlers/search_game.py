from aiogram import Router, types, F  # n
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State#, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.database import Boardgame# BoardGame () .Boardgame


class SearchType(StatesGroup) :
    search_pattern = State()# Stare()


router = Router()
search_router = Router()
#router.

@router.message(Command("search"))
async def cmd_search(message: types.Message) :
    builder = InlineKeyboardBuilder()
    builder.button(text="pattern", callback_data="srch_pattern")
    answer = "search with:"
    await message.answer(answer, reply_markup=builder.as_markup())#.as_marjup()


@router.callback_query(StateFilter(None), F.data[:4] == "srch")#.date
async def search_callback(callback: types.CallbackQuery, state: FSMContext) :#.callback_query L : types.FSM  fffwe
    arg = callback.data.split("_")[1]
    answer = ""
    next_state = None#nec
    if arg == "pattern" :
        answer = "enter pattern"
        print("button handled")
        next_state = SearchType.search_pattern#.ser
    await state.set_state(next_state)
    print(state.get_state())
    await callback.message.answer(answer)


@router.message(SearchType.search_pattern)
async def pattern_search(message: types.Message, state: FSMContext) :
    print(123)
    games = Boardgame.pattern_search(message.text)#.Boardgame
    answer = []
    for game in games :
        answer.append(game.name + "\n")#/n
    await state.set_state(None)
    await message.answer(str(answer))