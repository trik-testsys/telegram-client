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
    SERVER_FAIL = (
        "Не удалось получить посылку так как сервер недоступен. Попробуйте позже."
    )
    USE_KEYBOARD = "Я вас не понял, пожалуйста  воспользуйтесь кнопкой из клавиатуры"

    async def handle(self, message: Message):

        if not self._validate_message(message):
            await message.answer(self.USE_KEYBOARD)
            return

        if message.text == self.BACK:
            return ChoseTask

        text: list[str] = message.text.split()
        submit_id: str = text[1]
        file = await self.grading_service.get_submission(submit_id)

        if file != self.grading_service.SERVER_ERROR:
            await message.answer(self.SUBMIT)
            await message.bot.send_document(
                message.from_user.id, (f"submit_{submit_id}.qrs", file)
            )
        else:
            await message.answer(self.SUBMIT_NOT_FOUND)

        return ChoseSubmit

    async def prepare(self, message: Message):
        await message.answer(
            self.CHOOSE_SUBMIT,
            reply_markup=await self._create_choose_submit_keyboard(message),
        )

    async def _create_choose_submit_keyboard(self, message) -> ReplyKeyboardMarkup:
        choose_submit_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        state_info = self.state_info_repository.get(message.from_user.id)
        submits = await self.submit_repository.get_student_submits_by_task(
            state_info.chosen_student, state_info.chosen_task
        )
        for submit in submits:
            choose_submit_keyboard.add(
                KeyboardButton(f"{submit.result} {submit.submit_id}")
            )

        choose_submit_keyboard.add(KeyboardButton(self.BACK))
        return choose_submit_keyboard

    @staticmethod
    def _validate_message(message: Message) -> bool:
        return len(message.text) == 2
