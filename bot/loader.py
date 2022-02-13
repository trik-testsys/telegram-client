from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import peewee

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.data.StateInfoHolder import StateInfoHolder
from bot.utils.injector import Singleton
from config import BOT_TOKEN

bot = Singleton(Bot(token=BOT_TOKEN))
storage = Singleton(MemoryStorage())
scheduler = Singleton(AsyncIOScheduler())
db = Singleton(peewee.SqliteDatabase("data.sqlite"))
dp = Singleton(Dispatcher(bot, storage=storage))
stateInfoHolder = Singleton(StateInfoHolder())

