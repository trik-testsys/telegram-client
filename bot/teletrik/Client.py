import logging
from typing import List, Tuple, Coroutine, Callable, Any

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.teletrik.DI import Handler, get_handlers
from bot.teletrik.MainHandler import MainHandler


class Client:

    def __init__(self, api_key: str):
        self._bot: Bot = Bot(token=api_key)
        self._dp: Dispatcher = Dispatcher(self._bot)
        self._scheduler: AsyncIOScheduler = AsyncIOScheduler()
        self._scheduler_jobs: List[Tuple[Coroutine, int]] = []

    def run(self, log_level: int):
        logging.basicConfig(level=log_level, filename="bot.txt")
        self._add_scheduler_jobs()
        self._scheduler.start()
        self._dp.register_message_handler(self._create_handler(), content_types=ContentType.ANY)
        executor.start_polling(self._dp, skip_updates=True)

    def add_scheduler_job(self, job: Coroutine, interval: int):
        self._scheduler_jobs.append((job, interval))

    def _add_scheduler_jobs(self):
        for (job, interval) in self._scheduler_jobs:
            self._scheduler.add_job(job, "interval", seconds=interval)

    @staticmethod
    def _create_handler() -> Callable[[Message], Coroutine[Any, Any, None]]:
        handlers: List[Handler] = get_handlers()
        return MainHandler(handlers).main_handler


