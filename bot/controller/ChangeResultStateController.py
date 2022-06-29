from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from bot.controller.States import ChangeResult, TeacherMenu
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.UserRepository import UserRepository
from bot.service.GradingService import GradingService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(ChangeResult)
class ChoseTaskStateController(Controller):
    def __init__(self,
                 submit_repository: SubmitRepository,
                 user_repository: UserRepository,
                 grading_service: GradingService):
        self.submit_repository: SubmitRepository = submit_repository
        self.user_repository: UserRepository = user_repository
        self.grading_service: GradingService = grading_service

    BACK = "◂ Назад"
    INFO = "Отправьте id решения и новый вердикт\n" \
           "Пример: '1000001 +'"
    KEYBOARD = ReplyKeyboardMarkup().add(KeyboardButton(BACK))

    async def handle(self, message: Message):
        if message.text == self.BACK:
            return TeacherMenu

        (valid, error) = await self._validate_message(message)
        if not valid:
            await message.answer(error)
            return ChangeResult

        (submit_id, result) = self._parse_message(message)
        request_result = await self.grading_service.set_submission_status(submit_id, result)
        if request_result != f"Changed {submit_id} status to {result}.":
            await message.answer("Ошибка при обновлении вердикта, попробуйте позже")
            return ChangeResult
        await self.submit_repository.update_submit_result(submit_id, result)
        for teacher in await self.user_repository.get_by_role("teacher"):
            await message.bot.send_message(
                chat_id=teacher.telegram_id,
                text=f"Результат проверки {submit_id} изменен на '{result}' "
                     f"преподавателем {message.from_user.full_name}, id: {message.from_user.id}"
            )
        await message.answer("Вердикт обновлен")
        return ChangeResult

    async def prepare(self, message: Message):
        await message.answer(self.INFO, reply_markup=self.KEYBOARD)

    async def _validate_message(self, message: Message) -> (bool, str):
        text: list[str] = message.text.strip().split()

        if len(text) != 2:
            return False, "Я вас не понял, пожалуйста, проверьте данные"

        if not text[0].isdigit():
            return False, "id должен быть числом"

        if not text[1] in ["-", "+"]:
            return False, "Вердикт должен быть либо '+', либо '-'"

        if await self.submit_repository.get_submit_or_none(text[0]) is None:
            return False, "Решение с таким id не существует"

        return True, ""

    @staticmethod
    def _parse_message(message: Message) -> (str, str):
        text: list[str] = message.text.strip().split()
        return text[0], text[1]
