from aiogram import types

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.student_states import TaskMenuState, StudentMenuState
from bot.StateMachine.teacher_states import TeacherMenuState
from bot.config import STUDENTS, TEACHERS
from bot.loader import stateInfoHolder


class Commands:
    pass


class Messages:
    SUCCESS_AUTH_TEACHER = "Вы успешно авторизованы как преподаватель!"
    SUCCESS_AUTH_STUDENT = "Вы успешно авторизованы как ученик!"
    INCORRECT_CODE = "Ваш код некорректен, попробуйте еще раз"


class Keyboards:
    pass


async def handler(message: types.Message):

    if message.text in STUDENTS:
        await message.reply(Messages.SUCCESS_AUTH_STUDENT)
        stateInfoHolder.create(message.from_user.id, message.text)
        await StudentMenuState.prepare(message)
        await StateMachine.student_menu.set()

    elif message.text in TEACHERS:
        await message.reply(Messages.SUCCESS_AUTH_TEACHER)
        stateInfoHolder.create(message.from_user.id, message.text)
        await TeacherMenuState.prepare(message)
        await StateMachine.teacher_menu.set()

    else:
        await message.reply(Messages.INCORRECT_CODE)


async def prepare(message: types.Message):
    pass
