from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.teacher_states import TeacherMenuState, ChoseTaskState
from bot.config import STUDENTS
from bot.data.Submit import get_all_results_view, get_student_result, get_student_submits_by_task
import aiogram.utils.markdown as md

from bot.grading.GradingClient import get_submit
from bot.loader import stateInfoHolder, tasks, bot


class Commands:
    RESULTS = "Результаты"
    CHOOSE_SUBMIT = "Посылки по задаче"
    BACK = "Назад"


class Messages:
    SUBMIT = "Посылка ученика"


class Keyboards:


    async def create_CHOOSE_SUBMIT_KEYBOARD(self, message):
        CHOOSE_SUBMIT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        state_info = stateInfoHolder.get(message.from_user.id)
        submits = await get_student_submits_by_task(state_info.chosen_student, state_info.chosen_task)
        for submit in submits:
            print(submit)
            CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(f"{submit.result} {submit.submit_id}"))

        CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(Commands.BACK))
        return CHOOSE_SUBMIT_KEYBOARD


async def handler(message: types.Message):

    if message.text == Commands.BACK:
        await StateMachine.chose_task.set()
        await ChoseTaskState.prepare(message)
        return

    text = message.text.split()

    if len(text) != 2:
        return

    submit_id = text[1]
    await message.answer(Messages.SUBMIT)
    file = await get_submit(submit_id)
    await bot.send_document(message.from_user.id, (f'submit_{submit_id}.qrs', file))


async def prepare(message: types.Message):
    await message.answer(Commands.CHOOSE_SUBMIT, reply_markup=await Keyboards().create_CHOOSE_SUBMIT_KEYBOARD(message))
