from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.teacher_states import ChoseStudentState
from bot.config import STUDENTS
from bot.data.Submit import get_all_results_view
import aiogram.utils.markdown as md


class Commands:
    RESULTS = "Результаты"
    CHOOSE_STUDENT = "Ученики"
    UNKNOWN_COMMAND = "Неизвестная команда"
    BACK = "Назад"


class Messages:
    CHOOSE_ACTION = "Выберите действие"


class Keyboards:
    TEACHER_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(Commands.RESULTS),
        KeyboardButton(Commands.CHOOSE_STUDENT)
    )


async def handler(message: types.Message):
    match message.text:

        case Commands.RESULTS:
            results = await get_all_results_view()
            await message.answer(md.code(results), parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=Keyboards.TEACHER_MENU_KEYBOARD)

        case Commands.CHOOSE_STUDENT:
            await StateMachine.chose_student.set()
            await ChoseStudentState.prepare(message)

        case _:
            pass


async def prepare(message: types.Message):
    await message.reply(Messages.CHOOSE_ACTION, reply_markup=Keyboards.TEACHER_MENU_KEYBOARD)
