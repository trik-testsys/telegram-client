from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.teacher_states import TeacherMenuState, ChoseTaskState
from bot.config import STUDENTS
from bot.data.Submit import get_all_results_view
import aiogram.utils.markdown as md

from bot.loader import stateInfoHolder


class Commands:
    RESULTS = "Результаты"
    CHOOSE_STUDENT = "Ученики"
    BACK = "Назад"


class Messages:
    pass


class Keyboards:

    CHOOSE_STUDENT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
    for student in STUDENTS:
        CHOOSE_STUDENT_KEYBOARD.add(KeyboardButton(student))

    CHOOSE_STUDENT_KEYBOARD.add(KeyboardButton(Commands.BACK))


async def handler(message: types.Message):

    if message.text == Commands.BACK:
        await StateMachine.teacher_menu.set()
        await TeacherMenuState.prepare(message)
        return

    if message.text in STUDENTS:
        stateInfoHolder.get(message.from_user.id).chosen_student = message.text
        await StateMachine.chose_task.set()
        await ChoseTaskState.prepare(message)


async def prepare(message: types.Message):
    await message.answer(Commands.CHOOSE_STUDENT, reply_markup=Keyboards.CHOOSE_STUDENT_KEYBOARD)
