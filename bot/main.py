import logging
import asyncio
import loader
import Controller

from aiogram.utils import executor
from bot.data.Submit import init_database
from bot.grading import GradingClient


def main():
    logging.basicConfig(level=logging.DEBUG)
    init_database()
    asyncio.gather(GradingClient.start_polling())
    executor.start_polling(loader.dp, skip_updates=True)


if __name__ == '__main__':
    main()
