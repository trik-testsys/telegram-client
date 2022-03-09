from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.controller.StateController.States import States

import aiogram.utils.markdown as md

from bot.loader import dp
from bot.repository.SubmitRepository import SubmitRepository
from utils.injector import StateController, ChangeState


@StateController(States.teacher_menu, dp)
class TeacherMenuStateController:

    submitRepository = SubmitRepository

    RESULTS = "Результаты"
    CHOOSE_STUDENT = "Ученики"
    UNKNOWN_COMMAND = "Неизвестная команда"
    BACK = "Назад"

    CHOOSE_ACTION = "Выберите действие"

    TEACHER_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(RESULTS),
        KeyboardButton(CHOOSE_STUDENT)
    )

    @classmethod
    async def handler(cls, message: types.Message):
        match message.text:

            case cls.RESULTS:
                results = await cls.submitRepository.get_all_results_view()
                await message.answer(md.code(results), parse_mode=ParseMode.MARKDOWN_V2,
                                     reply_markup=cls.TEACHER_MENU_KEYBOARD)

            case cls.CHOOSE_STUDENT:
                await ChangeState(States.chose_student, message)
                await States.chose_student.set()

            case _:
                pass

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.reply(cls.CHOOSE_ACTION, reply_markup=cls.TEACHER_MENU_KEYBOARD)
