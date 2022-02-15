from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.controller.StateController.States import States
from bot.config import STUDENTS
from bot.loader import dp
from bot.repository.StateInfoRepository import StateInfoRepository
from utils.injector import StateController, ChangeState


@StateController(States.chose_student, dp)
class ChoseStudentStateController:

    stateInfoRepository = StateInfoRepository

    RESULTS = "Результаты"
    CHOOSE_STUDENT = "Ученики"
    BACK = "Назад"

    CHOOSE_STUDENT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
    for student in STUDENTS:
        CHOOSE_STUDENT_KEYBOARD.add(KeyboardButton(student))
    CHOOSE_STUDENT_KEYBOARD.add(KeyboardButton(BACK))

    @classmethod
    async def handler(cls, message: types.Message):

        if message.text == cls.BACK:
            await ChangeState(States.teacher_menu, message)

        if message.text in STUDENTS:
            cls.stateInfoRepository.get(message.from_user.id).chosen_student = message.text
            await ChangeState(States.chose_task, message)

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.answer(cls.CHOOSE_STUDENT, reply_markup=cls.CHOOSE_STUDENT_KEYBOARD)
