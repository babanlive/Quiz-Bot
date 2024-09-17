import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db import create_table


# Загрузим переменные окружения из файла .env
load_dotenv()

# Получаем токен из переменной окружения
API_TOKEN = os.getenv('API_TOKEN')

# Диспетчер
dp = Dispatcher()


async def main():
    # Создаем таблицу в базе данных
    await create_table()

    # Объект бота
    bot = Bot(token=API_TOKEN)

    # Запускаем процесс поллинга новых апдейтов
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
