from aiogram import types

from bot.Controller.StateController.States import States
from bot.loader import dp
from bot.utils.injector import CommandController, ChangeState


@CommandController(["start", "restart"], dp)
class StartCommandController:

    ASK_CODE = "Отправьте, пожалуйста, свой код!"

    @classmethod
    async def handler(cls, message: types.Message):
        await ChangeState(States.wait_auth, message)
        await message.answer(cls.ASK_CODE)
