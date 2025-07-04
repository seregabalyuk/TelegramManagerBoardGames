from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
  # для поиска
  wrote_find_text = State()
  # для add
  found_add_game = State()
  chose_place_add = State()
  # для search
  found_search_game = State()
  chose_show_all_search = State()
  ask_to_users = State()
  # для view
  open_view_games = State()
  # для ask
  get_answer_ask = State()
  # для return
  leased_shown = State()
  

  