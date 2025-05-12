from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
#from src.database import Boardgame# BoardGame () .Boardgame

from database import TypeBoardgame, User
from handlers.States import States
from handlers import ask

router = Router()


def get_buttons_with_info(game_info, data) :
  buttons = []
  if game_info is None :
    buttons.append([InlineKeyboardButton(text="Добавить в свои", callback_data=data + " add")])#"add to my games"
    buttons.append([InlineKeyboardButton(text="Добавить в список желаемого", callback_data=data + " wishlist")])#"add to wishlist"
  else :
    if not game_info[1] :
      buttons.append([InlineKeyboardButton(text="Добавть в свои(уже приобретено)", callback_data=data + " add")])#"add to my games(already bought)"
  buttons.append([InlineKeyboardButton(text="попросить", callback_data=data + " ask")])
  buttons.append([InlineKeyboardButton(text="закрыть", callback_data="close")])
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
        await state.clear()
        await state.set_state(None)
        await callback.message.edit_text("""
        Для повторной попытки поиска нажмите /add\nМожете ввести лишь часть названия.
        """)
    else :
        args = data.split()
        game = TypeBoardgame.load_by_id(int(args[0]))
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
        buttons = [[InlineKeyboardButton(text="Посмотреть, у кого есть", callback_data=data + " check_others")]]#"check, who own"
        add_buttons = get_buttons_with_info(game_info, data)
        for button in add_buttons :
            buttons.append(button)
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        answer = f"""
        Название: {game.name}
        Количество игроков: {game.min_players}-{game.max_players}
        Продолжительность игры: {game.playing_time()} мин.
        Возраст: {game.age}+
        статус: {game_status}
        """
        await state.set_state(States.chose_show_all_search)
    await callback.message.edit_text(answer, reply_markup=markup)


@router.callback_query(StateFilter(States.chose_show_all_search))
async def after_show(callback: types.CallbackQuery, state: FSMContext) :
    data = callback.data
    message = callback.message
    args = data.split()


    if args[-1] == "close" :
        buttons = []
        await state.clear()
        await state.set_state(None)#Nobe
        await callback.message.delete()
        return
    buttons = get_buttons_with_info(User.load(callback.from_user.id).check_game(int(args[0])), data)
    answer = ""
    if args[-1] == "check_others" : # or args[-1] == "ask"
        answer = ""#"doing somthing..."
        almost_everything = User.load(callback.from_user.id).get_friends(with_game_id=int(args[0]))
        with_game_str = "\n\nПользователи с этой игрой\n" #users, that has this game= [] <?
        wishlisted_str = "\nПользователи с этой игрой в списке желаний\n"#users, that has this game in their wishlist
        for row in almost_everything :
            if row[2] :
                with_game_str = with_game_str + row[3] + "(" + row[4] + ", "
                if row[1] is None :
                    with_game_str = with_game_str + "свободна)\n"#free
                else :
                    with_game_str = with_game_str + "занята\n"#not free
            else :
                wishlisted_str = wishlisted_str + row[3] + "(" + row[4] + ")\n"
        answer += with_game_str + wishlisted_str
    if args[-1] == "add" or args[-1] == "wishlist" : #else :  ar
        if User.load(callback.from_user.id).add_boardgame(int(args[0]), args[-1] == "add") : #
            answer = "Игра добавена"#"game added"
        else : #
            answer = "BRUH" #"somethings went wrong..."
    if args[-1] == "ask" : #
        almost_everything = User.load(callback.from_user.id).get_friends(with_game_id=int(args[0]))#message

        answer = "попросить у: " #
        for row in almost_everything :
            if row[1] is None and row[2] :
                buttons.append([InlineKeyboardButton(text=row[3], callback_data=args[0] + " " + str(row[5]))])
        await state.set_state(States.ask_to_users)

    await message.edit_text(message.text + "\n" + answer, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@router.callback_query(StateFilter(States.ask_to_users))
async def ask_to(callback: types.CallbackQuery, state: FSMContext) :
    args = callback.data.split()
    if args[0] == "close" :
        await state.clear()
        await state.set_state(None)
        await callback.message.delete()
    game = TypeBoardgame.load_by_id(int(args[0]))
    print(args)
    message = callback.message
    print(User.load(callback.from_user.id), User.load(int(args[1])), game.id, game.name)
    await state.clear()
    await state.set_state(None)
    await message.edit_text(message.text + "\n запpос отправлен")
    await ask.ask(User.load(callback.from_user.id), User.load(int(args[1])), game.id, game.name)
