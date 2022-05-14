from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.controller.StateController.States import States
from bot.loader import bot, dp
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.service.GradingService import GradingService
from utils.injector import StateController, ChangeState


@StateController(States.chose_submit, dp)
class ChoseSubmitStateController:

    submitRepository = SubmitRepository
    stateInfoRepository = StateInfoRepository
    gradingService = GradingService

    RESULTS = "Результаты"
    CHOOSE_SUBMIT = "Попытки по задаче ▸"
    BACK = "◂ Назад"

    SUBMIT = "Посылка ученика"
    SUBMIT_NOT_FOUND = "Не удалось получить посылку так как сервер недоступен. Попробуйте позже."

    @classmethod
    async def create_CHOOSE_SUBMIT_KEYBOARD(cls, message):
        CHOOSE_SUBMIT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        state_info = cls.stateInfoRepository.get(message.from_user.id)
        submits = await cls.submitRepository.get_student_submits_by_task(state_info.chosen_student, state_info.chosen_task)
        for submit in submits:
            CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(f"{submit.result} {submit.submit_id}"))

        CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(cls.BACK))
        return CHOOSE_SUBMIT_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):

        if message.text == cls.BACK:
            await ChangeState(States.chose_task, message)
            return

        text = message.text.split()

        if len(text) != 2:
            return

        submit_id = text[1]
        await message.answer(cls.SUBMIT)
        file = await cls.gradingService.get_submit(submit_id)
        if file != cls.gradingService.ERROR:
            await bot.send_document(message.from_user.id, (f'submit_{submit_id}.qrs', file))
        else:
            await message.answer(cls.SUBMIT_NOT_FOUND)

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.answer(cls.CHOOSE_SUBMIT, reply_markup=await cls.create_CHOOSE_SUBMIT_KEYBOARD(message))
