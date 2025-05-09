from aiogram import Router, types, F  # n
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
#from src.database import Boardgame# BoardGame () .Boardgame
from src.database import GameBoard, User


class SearchType(StatesGroup) :
    search_pattern = State()

class States(StatesGroup) :
    started = State()
    found = State()
    shown = State()

router = Router()

def create_buttons(games) :
    buttons = []
    for (id, name) in games :
        buttons.append([InlineKeyboardButton(text=name, callback_data=str(id) + " " + name)])#
    buttons.append([InlineKeyboardButton(text="nothing", callback_data="not found")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_buttons_with_info(game_info, data) :
    buttons = []
    if game_info is None :
        buttons.append([InlineKeyboardButton(text="add to my games", callback_data=data + " add")])
        buttons.append([InlineKeyboardButton(text="add to wishlist", callback_data=data + " wishlist")])
    else :
        if not game_info[1] :
            buttons.append([InlineKeyboardButton(text="add to my games(already bought)", callback_data=data + " add")])

        #else :
    return buttons

@router.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext) :
    answer = "enter pattern"
    await state.set_state(States.started)
    await message.answer(answer)


# @router.callback_query(StateFilter(None), F.data[:4] == "srch")
# async def search_callback(callback: types.CallbackQuery, state: FSMContext) :
#     arg = callback.data.split("_")[1]
#     answer = ""
#     next_state = None#nec
#     if arg == "pattern" :
#         answer = "enter pattern"
#         print("button handled")
#         next_state = SearchType.search_pattern
#     await state.set_state(next_state)
#     print(state.get_state())
#     await callback.message.answer(answer)


@router.message(States.started)
async def pattern_search(message: types.Message, state: FSMContext) :
    games = GameBoard.find(message.text)
    answer = ""
    if len(games) == 0 :
        await state.clear()
        answer = "coudnt find anything"
    else :
        await state.set_state(States.found)
        answer = "found games:"
    await message.answer(answer, reply_markup=create_buttons(games))


@router.callback_query(StateFilter(States.found))#e
async def selected_callback(callback: types.CallbackQuery, state: FSMContext ) :
    data = callback.data
    message = callback.message
    answer = ""
    markup = None
    if data == "not found" :
        await state.clear()
        answer = "You can try again with the part of name"
    else :
        args = data.split()
        game = GameBoard.load(int(args[0]))
        game_info = User.load(callback.from_user.id).check_game(game.id)
        game_status = ""
        if game_info is None :
            game_status = "not wishlisted"
        else :
            if game_info[1] :
                game_status = "your own"
            else :
                game_status = "whishlisted"
        print(game.name, game.playing_time, args[0], game_info)
        buttons = [[InlineKeyboardButton(text="check, who own", callback_data=data + " check_others")]]
        add_buttons = get_buttons_with_info(game_info, data)
        for button in add_buttons :
            buttons.append(button)
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        answer = "title: " + game.name + "\n minimum players: " + str(game.min_players) + "\nmaximum players: " + str(game.max_players) + "\nsession duration: " + str(game.playing_time) + " min\nstatus: " + game_status + " ..."
        await state.set_state(States.shown)
    await message.edit_text(answer, reply_markup=markup)

@router.callback_query(StateFilter(States.shown))
async def after_show(callback: types.CallbackQuery, state: FSMContext) :
    data = callback.data
    message = callback.message
    args = data.split()
    buttons = get_buttons_with_info(User.load(callback.from_user.id).check_game(int(args[0])), data)
    answer = ""
    if args[-1] == "check_others" :
        #TO DO TODA
        answer = "doing somthing..."
        almost_everything = User.load(callback.from_user.id).get_friends(with_game_id=int(args[0]))
        with_game_str = "\n\nusers, that has this game\n" #= [] <?
        wishlisted_str = "\nusers, that has this game in their wishlist\n"
        for row in almost_everything :
            if row[2] :
                with_game_str = with_game_str + row[3] + "(" + row[4] + ", "
                if row[1] is None :
                    with_game_str = with_game_str + "free)\n"
                else :
                    with_game_str = with_game_str + "not free\n"
            else :
                wishlisted_str = wishlisted_str + row[3] + "(" + row[4] + ")\n"
        answer += with_game_str + wishlisted_str
    else :
        if User.load(callback.from_user.id).add_boardgame(int(args[0]), args[2] == "add") : #
            answer = "game added"
        else : #
            answer = "somethings went wrong..."
    await message.edit_text(message.text + "\n" + answer, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
