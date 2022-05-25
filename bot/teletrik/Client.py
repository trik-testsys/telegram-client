import logging
from typing import List, Coroutine, Callable, Any

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType, BotCommand
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.conf import PATH_TO_LOGS
from bot.teletrik.DI import Handler, get_handlers, get_jobs
from bot.teletrik.MainHandler import MainHandler


class Client:

    def __init__(self, api_key: str):
        self._bot: Bot = Bot(token=api_key)
        self._dp: Dispatcher = Dispatcher(self._bot)
        self._scheduler: AsyncIOScheduler = AsyncIOScheduler()

    def run(self, log_level: int):
        logging.basicConfig(level=log_level, filename=PATH_TO_LOGS)
        self._dp.register_message_handler(self._create_handler(), content_types=ContentType.ANY)
        self._add_scheduler_jobs()
        self._scheduler.start()
        executor.start_polling(self._dp, skip_updates=True)

    def _add_scheduler_jobs(self):
        for job in get_jobs():
            self._scheduler.add_job(job, "interval", seconds=30)

    @staticmethod
    def _create_handler() -> Callable[[Message], Coroutine[Any, Any, None]]:
        handlers: List[Handler] = get_handlers()
        return MainHandler(handlers).main_handler
