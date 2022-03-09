from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.controller.StateController.States import States

from bot.loader import bot, dp
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.service.GradingService import GradingService

from utils.injector import StateController, ChangeState


@StateController(States.submit, dp)
class SubmitStateController:

    stateInfoRepository = StateInfoRepository
    gradingService = GradingService

    BACK = "Назад"
    SEND_FILE = "Отправьте файл с решением или нажмите <<Назад>>"
    SENT = "Решение отправлено"
    NOT_SENT = "Решение не отправлено так как сервер проверки недоступен. Попробуйте позже"
    ERROR_NOT_FILE = "Пожалуйста, отправьте файл"
    BACK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BACK))

    @classmethod
    async def handler(cls, message: types.Message):
        print("lmao")
        if message.text == cls.BACK:
            await ChangeState(States.task_menu_student, message)
            return

        if message.document is None:
            await message.answer(cls.ERROR_NOT_FILE)
            return

        document_id = message.document.file_id
        file = await bot.download_file_by_id(document_id)
        state_info = cls.stateInfoRepository.get(message.from_user.id)
        print("lol")
        submit_id = await cls.gradingService.send_task(state_info.chosen_task, state_info.user_id, file)

        if submit_id != cls.gradingService.ERROR:
            await message.answer(f"{cls.SENT}, ID посылки: {submit_id}")
        else:
            await message.answer(f"{cls.NOT_SENT}")

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.reply(cls.SEND_FILE, reply_markup=cls.BACK_KEYBOARD)
