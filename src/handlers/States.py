from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
  # для поиска игр
  wrote_find_game = State()
  # для поиска друзей
  wrote_find_user = State()
  

  