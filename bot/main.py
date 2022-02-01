import logging
import time

from aiogram import types
from aiogram.utils import executor

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.register_all_handlers import register_all_handlers
from bot.data.Submit import init_database, test_database
from bot.grading import GradingClient
from bot.grading.GradingServer import test_grading
from loader import dp

import asyncio


@dp.message_handler(commands=['start', 'restart'], state="*")
async def send_welcome(message: types.Message):
    await StateMachine.wait_auth.set()
    await message.answer("Отправьте, пожалуйста, свой код!")


logging.basicConfig(level=logging.DEBUG)


def main():
    register_all_handlers(dp)
    init_database()
    asyncio.gather(GradingClient.start_polling())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
