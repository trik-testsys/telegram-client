import logging
import asyncio
import loader
import Controller

from aiogram.utils import executor
from bot.data.Submit import init_database
from bot.grading.GradingClient import update_all_submits_status


def main():
    logging.basicConfig(level=logging.DEBUG)
    init_database()
    loader.scheduler.add_job(update_all_submits_status, "interval", seconds=30)
    loader.scheduler.start()
    executor.start_polling(loader.dp, skip_updates=True)


if __name__ == '__main__':
    main()
