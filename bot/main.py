import logging
import loader
import controller

from aiogram.utils import executor
from bot.service.GradingService import GradingService


def main():
    logging.basicConfig(level=logging.DEBUG)
    loader.scheduler.add_job(GradingService.update_all_submits_status, "interval", seconds=30)
    loader.scheduler.start()
    executor.start_polling(loader.dp, skip_updates=True)


if __name__ == '__main__':
    main()
