from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database import User

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
  first_name = message.from_user.first_name
  last_name = message.from_user.last_name
  username = message.from_user.username
  id = message.from_user.id

  try:
    User.get(id, username)
  except:
    print ("cannot to load")
  
  answer = f"""
  Привет {first_name} {last_name}\\!
  Я бот, который поможет отслеживать настольные игры твои и твоих друзей\\!
  ```c++
    int main() {{
    }}
  ```
  """
  await message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)