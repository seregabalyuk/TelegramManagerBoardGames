from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database import GameBoard

router = Router()

class Add(StatesGroup):
  gamename = State()


@router.message(Command("add"))
async def cmd_start(message: types.Message, state: FSMContext):
  await state.set_state(Add.gamename)
  await message.answer("Напишите название настольной игры")


@router.message(Add.gamename)
async def process_name(message: types.Message, state: FSMContext):
  gamename = message.text
  # games = GameBoard.find(gamename)
  await state.clear()
  await message.answer(f"Я не нашёл {gamename}")
