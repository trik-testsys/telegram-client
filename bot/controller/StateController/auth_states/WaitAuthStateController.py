from aiogram import types

from bot.controller.StateController.States import States
from bot.loader import dp
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.UserRepository import UserRepository
from utils.injector import StateController, ChangeState


@StateController(States.wait_auth, dp)
class WaitAuthStateController:

    stateInfoRepository = StateInfoRepository
    userRepository = UserRepository

    SUCCESS_AUTH_TEACHER = "Вы успешно авторизованы как преподаватель!"
    SUCCESS_AUTH_STUDENT = "Вы успешно авторизованы как ученик!"
    INCORRECT_CODE = "Ваш код некорректен, попробуйте еще раз"

    @classmethod
    async def handler(cls, message: types.Message):

        if await cls.userRepository.is_student(message.text):
            await message.reply(cls.SUCCESS_AUTH_STUDENT)
            cls.stateInfoRepository.create(message.from_user.id, message.text)
            await ChangeState(States.student_menu, message)

        elif await cls.userRepository.is_teacher(message.text):
            await message.reply(cls.SUCCESS_AUTH_TEACHER)
            cls.stateInfoRepository.create(message.from_user.id, message.text)
            await ChangeState(States.teacher_menu, message)

        else:
            await message.reply(cls.INCORRECT_CODE)

    @classmethod
    async def prepare(cls, message: types.Message):
        pass
