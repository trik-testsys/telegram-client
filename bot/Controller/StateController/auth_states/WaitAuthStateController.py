from aiogram import types

from bot import loader
from bot.Controller.StateController.States import States
from bot.config import STUDENTS, TEACHERS
from bot.loader import stateInfoHolder, dp
from bot.utils.injector import StateController, ChangeState


@StateController(States.wait_auth, dp)
class WaitAuthStateController:

    SUCCESS_AUTH_TEACHER = "Вы успешно авторизованы как преподаватель!"
    SUCCESS_AUTH_STUDENT = "Вы успешно авторизованы как ученик!"
    INCORRECT_CODE = "Ваш код некорректен, попробуйте еще раз"

    @classmethod
    async def handler(cls, message: types.Message):

        if message.text in STUDENTS:
            await message.reply(cls.SUCCESS_AUTH_STUDENT)
            stateInfoHolder.create(message.from_user.id, message.text)
            await ChangeState(States.student_menu, message)

        elif message.text in TEACHERS:
            await message.reply(cls.SUCCESS_AUTH_TEACHER)
            stateInfoHolder.create(message.from_user.id, message.text)
            await ChangeState(States.teacher_menu, message)

        else:
            await message.reply(cls.INCORRECT_CODE)

    @classmethod
    async def prepare(cls, message: types.Message):
        pass
