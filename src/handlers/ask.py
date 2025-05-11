import bot_loader as bl
import asyncio


async def ask(from_user, to_user, game_id, game_name):
  await bl.bot.send_message(
    chat_id = to_user.telegram_id,
    text = f"У тебя попросил {game_name} пользователь с именем {from_user.name}"
  )