import asyncio
import logging
import os
import string
import sys
import random
from database_postgres import init_pg, insert_data, get_user_links
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.environ.get('API_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт!\nЯ бот, який скорочує посилання.\n")


@dp.message_handler(commands=['my_links'])
async def my_links(message: types.Message):
    links = await get_user_links(message.from_user.id)
    await message.reply('\n'.join(links))


@dp.message_handler()
async def echo(message: types.Message):
    link = message.text
    if link.startswith('http') or link.startswith('https'):
        characters = string.ascii_lowercase + string.digits
        new_link = ''.join(random.choice(characters) for i in range(6))
        await insert_data(link, new_link, message.from_user.id)
        await message.answer(f'http://127.0.0.1:8001/{new_link}')
    else:
        await message.answer('Неправильне посилання')


if __name__ == '__main__':
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    executor.start_polling(dp, skip_updates=True)
