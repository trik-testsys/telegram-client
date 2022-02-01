from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.teacher_states import TeacherMenuState, ChoseStudentState, ChoseSubmitState
from bot.config import STUDENTS
from bot.data.Submit import get_all_results_view, get_student_result
import aiogram.utils.markdown as md

from bot.loader import stateInfoHolder, tasks


class Commands:
    RESULTS = "Результаты"
    CHOOSE_TASK = "Задачи ученика"
    BACK = "Назад"


class Messages:
    pass


class Keyboards:
    async def create_CHOOSE_TASK_KEYBOARD(self, message):

        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        student_result = await get_student_result(stateInfoHolder.get(message.from_user.id).chosen_student)
        for task_name in student_result.keys():
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f"{student_result[task_name]} {task_name}"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(Commands.BACK))
        return CHOOSE_TASK_KEYBOARD


async def handler(message: types.Message):

    if message.text == Commands.BACK:
        await StateMachine.chose_student.set()
        await ChoseStudentState.prepare(message)
        return

    text = message.text.split()

    if len(text) != 2:
        return

    task_name = text[1]
    if task_name not in tasks:
        return

    stateInfoHolder.get(message.from_user.id).chosen_task = task_name
    await StateMachine.chose_submit.set()
    await ChoseSubmitState.prepare(message)


async def prepare(message: types.Message):
    await message.answer(Commands.CHOOSE_TASK, reply_markup=await Keyboards().create_CHOOSE_TASK_KEYBOARD(message))
