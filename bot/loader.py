from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import peewee

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.injector import Singleton
from config import BOT_TOKEN

bot = Singleton(Bot(token=BOT_TOKEN))
storage = Singleton(MemoryStorage())
scheduler = Singleton(AsyncIOScheduler())

db = Singleton(peewee.SqliteDatabase("../submit.sqlite", pragmas={
    'journal_mode': 'wal',
    'synchronous': 'normal'
}))

dp = Singleton(Dispatcher(bot, storage=storage))

