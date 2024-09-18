import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db import create_table
from handlers import register_handlers


load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

dp = Dispatcher()


async def main():
    await create_table()

    register_handlers(dp)

    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
