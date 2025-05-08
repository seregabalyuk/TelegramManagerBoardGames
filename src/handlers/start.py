from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import User, Group

router = Router()



@router.message(Command("start"))
async def cmd_start(message: types.Message):
  first_name = message.from_user.first_name
  last_name = message.from_user.last_name
  username = message.from_user.username
  id = message.from_user.id

  args = message.text.split()
  user = None
  registreted = False
  answer = ""

  # регистрация и добавление в группу
  try:
    user = User.get(id, username, registreted)
  except:
    print ("cannot load user. with error:" + repr(error))
  if (user == None):
    answer = f"""
    Привет \\!
    У нас технические шоколадки
    База данных полетела(
    """
  else:
    if registreted:
      answer = f"""
      Привет {first_name} {last_name}\\!
      Я бот, который поможет отслеживать настольные игры твои и твоих друзей\\!"""
    else:
      answer = f"""Привет {first_name} {last_name}\\!"""
    if len(args) > 1:
      param = args[1].split(sep='_')
      group_id = int(param[0])
      password = int(param[1])
      group = None
      try:
        group = Group.load(group_id, password)
        if group.contain(user):
          answer += "\n" + f"Вы уже состоите в {group.title}\\!"
        else:
          group.add(user)
          answer += "\n" + f"Вы присоединились к {group.title}\\!"
      except Exception as error:
        print ("cannot load group. with error:" + repr(error))
        answer += "\n" + f"Я не смог добавить вас в группу\\."

  await message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)
  
      
      