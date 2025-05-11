from aiogram import Router, types, F  # n
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
#from src.database import Boardgame# BoardGame () .Boardgame

from database import GameBoard, User
from handlers.States import States


router = Router()


def get_buttons_with_info(game_info, data) :
  buttons = []
  if game_info is None :
    buttons.append([InlineKeyboardButton(text="add to my games", callback_data=data + " add")])
    buttons.append([InlineKeyboardButton(text="add to wishlist", callback_data=data + " wishlist")])
  else :
    if not game_info[1] :
      buttons.append([InlineKeyboardButton(text="add to my games(already bought)", callback_data=data + " add")])
  return buttons



@router.message(Command("search"))
async def catcher(message: types.Message, state: FSMContext):
  await state.update_data(command="search")
  await state.set_state(States.wrote_find_text)
  await message.answer("Напишите название настольной игры")


@router.callback_query(StateFilter(States.found_search_game))
async def selected_callback(callback: types.CallbackQuery, state: FSMContext ) :
    data = callback.data
    answer = ""
    markup = None
    if data == "not found" :
       if data == "not found":
        await state.clear()
        await callback.message.edit_text("""
        Для повторной попытки поиска нажмите /add\nМожете ввести лишь часть названия.
        """)
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
        await state.set_state(States.chose_show_all_search)
    await callback.message.edit_text(answer, reply_markup=markup)


@router.callback_query(StateFilter(States.chose_show_all_search))
async def after_show(callback: types.CallbackQuery, state: FSMContext) :
    data = callback.data
    message = callback.message
    args = data.split()
    buttons = get_buttons_with_info(User.load(callback.from_user.id).check_game(int(args[0])), data)
    answer = ""
    if args[-1] == "check_others" :
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
