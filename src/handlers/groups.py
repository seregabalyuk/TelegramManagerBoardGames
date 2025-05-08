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

  group = Group.create(chat.id, chat.title)

  bot_link = f"https://t.me/BoardGameManagerBot?start={group.id}"
  print(bot_link)
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
  print(f"Меня удалили из чата {chat.title} (ID: {chat.id})")