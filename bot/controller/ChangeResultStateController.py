from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from bot.controller.States import ChangeResult, TeacherMenu
from bot.repository.SubmitRepository import SubmitRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(ChangeResult)
class ChoseTaskStateController(Controller):
    def __init__(self, submit_repository: SubmitRepository):
        self.submit_repository: SubmitRepository = submit_repository

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

        await self.submit_repository.update_submit_result(submit_id, result)
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
