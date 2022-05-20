from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

from bot.controller.States import SubmitTask, TaskMenu
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.service.GradingService import GradingService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(SubmitTask)
class SubmitStateController(Controller):

    def __init__(self, state_info_repository: StateInfoRepository, grading_service: GradingService):
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.grading_service: GradingService = grading_service

    BACK = "◂ Назад"
    SEND_FILE = "Отправьте файл с решением или нажмите <<Назад>>"
    SENT = "Решение отправлено"
    NOT_SENT = "Решение не отправлено так как сервер проверки недоступен. Попробуйте позже"
    ERROR_NOT_FILE = "Пожалуйста, отправьте файл"
    BACK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BACK))

    async def handle(self, message: Message):
        if message.text == self.BACK:
            return TaskMenu

        if message.document is None:
            await message.answer(self.ERROR_NOT_FILE)
            return SubmitTask

        document_id = message.document.file_id
        file = await message.bot.download_file_by_id(document_id)
        state_info = self.state_info_repository.get(message.from_user.id)
        submit_id = await self.grading_service.send_task(state_info.chosen_task, state_info.user_id, file)

        if submit_id != self.gradingService.ERROR:
            await message.answer(f"{self.SENT}, ID попытки: {submit_id}")
            return TaskMenu
        else:
            await message.answer(f"{self.NOT_SENT}")
            return SubmitTask

    async def prepare(self, message: Message):
        await message.answer(self.SEND_FILE, reply_markup=self.BACK_KEYBOARD)
