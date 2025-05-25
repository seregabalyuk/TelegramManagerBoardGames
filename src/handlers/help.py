from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message) :
    answer = "Телеграм-бот для упращения и повышения удобства заимствования настольноых игр\nВот доступные комманды"
    answer += "\n/add - добавить игру в свою колекцию или вишлист"
    answer += "\n/return - вернуть позаимствованную игру"
    answer += "\n/search - найти игру по названию"
    answer += "\n/start - запуск бота и регистрация"
    answer += "\n/view - просмотр информации о своих играх, друзьях, группах"
    await message.answer(answer)