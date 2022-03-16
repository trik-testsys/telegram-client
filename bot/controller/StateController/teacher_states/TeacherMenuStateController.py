from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.controller.StateController.States import States

import aiogram.utils.markdown as md

from bot.loader import dp, bot
from bot.repository.SubmitRepository import SubmitRepository
from utils.injector import StateController, ChangeState


@StateController(States.teacher_menu, dp)
class TeacherMenuStateController:
    submitRepository = SubmitRepository

    RESULTS = "Сводная статистика"
    FULL_RESULTS = "Полная статистика"

    CHOOSE_STUDENT = "Ученики ▸"
    UNKNOWN_COMMAND = "Неизвестная команда"
    BACK = "◂ Назад"

    CHOOSE_ACTION = "Выберите действие"

    TEACHER_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(RESULTS),
        KeyboardButton(FULL_RESULTS),
        KeyboardButton(CHOOSE_STUDENT)
    )

    @classmethod
    async def handler(cls, message: types.Message):
        match message.text:

            case cls.RESULTS:
                results = await cls.submitRepository.get_stat_view()
                await message.answer(results, reply_markup=cls.TEACHER_MENU_KEYBOARD)

            case cls.FULL_RESULTS:
                results = await cls.submitRepository.get_all_results_view()
                await bot.send_document(message.from_user.id, ('results.html', results))
                await message.answer("Результаты", reply_markup=cls.TEACHER_MENU_KEYBOARD)

            case cls.CHOOSE_STUDENT:
                await ChangeState(States.chose_student, message)
                await States.chose_student.set()

            case _:
                await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
                pass

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.reply(cls.CHOOSE_ACTION, reply_markup=cls.TEACHER_MENU_KEYBOARD)
