from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.student_states import StudentMenuState, TaskMenuState
from bot.data.Submit import get_student_submits_view
from bot.grading import GradingServer, GradingClient
from bot.loader import stateInfoHolder, tasks, bot
import aiogram.utils.markdown as md


class Commands:
    BACK = "Назад"


class Messages:
    SEND_FILE = "Отправьте файл с решением или нажмите <<Назад>>"
    SENT = "Решение отправлено"


class Keyboards:
    BACK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(Commands.BACK))


async def handler(message: types.Message):

    if message.text == Commands.BACK:
        await TaskMenuState.prepare(message)
        await StateMachine.task_menu_student.set()
        return

    document_id = message.document.file_id
    file = await bot.download_file_by_id(document_id)
    state_info = stateInfoHolder.get(message.from_user.id)
    submit_id = await GradingClient.send_task(state_info.chosen_task, state_info.user_id, file)
    await message.answer(f"{Messages.SENT}, ID посылки: {submit_id}")


async def prepare(message: types.Message):
    await message.reply(Messages.SEND_FILE, reply_markup=Keyboards.BACK_KEYBOARD)
