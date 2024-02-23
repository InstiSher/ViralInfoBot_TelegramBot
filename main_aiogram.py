import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.types.web_app_info import WebAppInfo
from config import token

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = [
        [types.KeyboardButton(text='Открыть веб страницу', web_app=WebAppInfo(url='https://itproger.com'))]
        ]
    markup = types.ReplyKeyboardMarkup(keyboard=keyboard)
    await message.answer('Привет, мой друг!', reply_markup=markup)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())