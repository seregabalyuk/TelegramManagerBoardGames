import bot_loader as bl
import asyncio


async def main():
  await bl.set_bot_commands(bl.bot)
  await bl.dp.start_polling(bl.bot)


if __name__ == "__main__":
  asyncio.run(main())

