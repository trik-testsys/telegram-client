from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.injector import Singleton

bot = Singleton(Bot(token=""))
storage = Singleton(MemoryStorage())
scheduler = Singleton(AsyncIOScheduler())
dp = Singleton(Dispatcher(bot, storage=storage))
