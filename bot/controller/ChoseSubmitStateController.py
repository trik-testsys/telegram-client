from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from bot.controller.States import ChoseSubmit, ChoseTask
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.service.GradingService import GradingService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(ChoseSubmit)
class ChoseSubmitStateController(Controller):
    def __init__(
        self,
        submit_repository: SubmitRepository,
        state_info_repository: StateInfoRepository,
        grading_service: GradingService,
    ):
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.grading_service: GradingService = grading_service

    RESULTS = "Результаты"
    CHOOSE_SUBMIT = "Попытки по задаче ▸"
    BACK = "◂ Назад"
    SUBMIT = "Посылка ученика"
    SUBMIT_NOT_FOUND = (
        "Не удалось получить посылку так как сервер недоступен. Попробуйте позже."
    )

    async def create_CHOOSE_SUBMIT_KEYBOARD(self, message):
        CHOOSE_SUBMIT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        state_info = self.state_info_repository.get(message.from_user.id)
        submits = await self.submit_repository.get_student_submits_by_task(
            state_info.chosen_student, state_info.chosen_task
        )
        for submit in submits:
            CHOOSE_SUBMIT_KEYBOARD.add(
                KeyboardButton(f"{submit.result} {submit.submit_id}")
            )

        CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(self.BACK))
        return CHOOSE_SUBMIT_KEYBOARD

    async def handle(self, message: Message):

        if message.text == self.BACK:
            return ChoseTask

        text = message.text.split()

        if len(text) != 2:
            return

        submit_id = text[1]
        await message.answer(self.SUBMIT)
        file = await self.grading_service.get_submission(submit_id)
        if file != self.grading_service.ERROR:
            await message.bot.send_document(
                message.from_user.id, (f"submit_{submit_id}.qrs", file)
            )
        else:
            await message.answer(self.SUBMIT_NOT_FOUND)

        return ChoseSubmit

    async def prepare(self, message: Message):
        await message.answer(
            self.CHOOSE_SUBMIT,
            reply_markup=await self.create_CHOOSE_SUBMIT_KEYBOARD(message),
        )
