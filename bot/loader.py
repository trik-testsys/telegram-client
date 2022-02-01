from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import peewee

from bot.data.StateInfoHolder import StateInfoHolder
from bot.data.task_loader import load_tasks
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
db = peewee.SqliteDatabase("data.sqlite")
dp = Dispatcher(bot, storage=storage)
tasks = load_tasks("./bot/tasks")
stateInfoHolder = StateInfoHolder()

