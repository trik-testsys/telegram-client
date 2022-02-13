from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.Controller.StateController.States import States
from bot.data.Submit import get_student_submits_view
from bot.grading import GradingClient
from bot.loader import stateInfoHolder, bot, dp

from bot.utils.injector import StateController, ChangeState


@StateController(States.submit, dp)
class SubmitStateController:

    BACK = "Назад"

    SEND_FILE = "Отправьте файл с решением или нажмите <<Назад>>"
    SENT = "Решение отправлено"

    BACK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BACK))

    @classmethod
    async def handler(cls, message: types.Message):
        if message.text == cls.BACK:
            await ChangeState(States.task_menu_student, message)
            return

        document_id = message.document.file_id
        file = await bot.download_file_by_id(document_id)
        state_info = stateInfoHolder.get(message.from_user.id)
        submit_id = await GradingClient.send_task(state_info.chosen_task, state_info.user_id, file)
        await message.answer(f"{cls.SENT}, ID посылки: {submit_id}")

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.reply(cls.SEND_FILE, reply_markup=cls.BACK_KEYBOARD)
