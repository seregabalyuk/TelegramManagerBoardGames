from aiogram import Bot, Router, types
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

from database import Group


router = Router()

# Добавление в чат
@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_added_to_chat(event: types.ChatMemberUpdated):
  chat = event.chat
  group = None
  try:
    group = Group.create(chat.id, chat.title)
    print(f"bot add to chat id={chat.id} title={chat.title}")
  except Exception as error:
    print ("cannot create group. with error:" + repr(error))

  if group == None:
    bot_link = f"https://www.youtube.com/watch?v=xvFZjo5PgG0&pp=0gcJCdgAo7VqN5tD"
  else:
    bot_link = f"https://t.me/BoardGameManagerBot?start={group.id}_{group.password}"

  builder = InlineKeyboardBuilder()
  builder.button(
    text="Добавиться в группу", 
    url=bot_link
  )
  answer = f"""
  Привет\\!
  Вы можете перейти по ссылке и добавиться в группу
  """
  await event.answer(
    answer,
    reply_markup=builder.as_markup(),
    parse_mode=ParseMode.MARKDOWN_V2
  )



# Удаление из чата
@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def bot_removed_from_chat(event: types.ChatMemberUpdated):
  chat = event.chat
  try:
    group = Group.create(chat.id, chat.title)
    group.delete()
    print(f"bot delete from chat id={chat.id} title={chat.title}")
  except Exception as error:
    print ("cannot delete group. with error:" + repr(error))



# Добавление нового участника
# @router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
# async def handle_new_member(event: types.ChatMemberUpdated):
#   chat = event.chat
#   user = event.new_chat_member.user
#   try:
#     group = Group.create(chat.id, chat.title)
#     print(f"bot add to chat id={chat.id} title={chat.title}")
#   except Exception as error:
#     print ("cannot not found group. with error:" + repr(error))

#   if group == None:
#     bot_link = f"https://www.youtube.com/watch?v=xvFZjo5PgG0&pp=0gcJCdgAo7VqN5tD"
#   else:
#     bot_link = f"https://t.me/BoardGameManagerBot?start={group.id}_{group.password}"

#   builder = InlineKeyboardBuilder()
#   builder.button(
#     text="Добавиться в группу", 
#     url=bot_link
#   )
#   answer = f"""
#   Привет {user.first_name} {user.last_name}\\!
#   Присоеденяйся к группе настолок \\:D
#   """
#   await event.answer(
#     answer,
#     reply_markup=builder.as_markup(),
#     parse_mode=ParseMode.MARKDOWN_V2
#   )