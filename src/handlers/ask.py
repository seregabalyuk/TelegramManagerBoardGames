import bot_loader as bl
import asyncio


async def ask(from_user, to_user, game):
  await bl.send_message(
    chat_id = to_user.id,
    text = f"У тебя попросил {game.name} пользователь с именем {from_user.name}"
  )