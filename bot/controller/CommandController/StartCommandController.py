from aiogram import types

from bot.controller.StateController.States import States
from bot.loader import dp
from utils.injector import CommandController, ChangeState


@CommandController(["start"], dp)
class StartCommandController:

    ASK_CODE = "Введите свой логин"

    @classmethod
    async def handler(cls, message: types.Message):
        await ChangeState(States.wait_auth, message)
        await message.answer(cls.ASK_CODE)
