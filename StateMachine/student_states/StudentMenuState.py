from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.student_states import TaskMenuState
from bot.data.Submit import get_student_result
from bot.loader import stateInfoHolder, tasks


class Commands:
    UPDATE = "Обновить"


class Messages:
    CHOOSE_ACTION = "Выберите действие"


class Keyboards:
    async def create_CHOOSE_TASK_KEYBOARD(self, student):
        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await get_student_result(student)

        for task_name in results.keys():
            result = results[task_name]
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f"{result} {task_name}"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(Commands.UPDATE))

        return CHOOSE_TASK_KEYBOARD


async def handler(message: types.Message):
    match message.text:

        case Commands.UPDATE:
            await prepare(message)

        case _:
            info = message.text.split()
            if len(info) != 2:
                return
            if info[1] in tasks.keys():
                stateInfoHolder.get(message.from_user.id).chosen_task = info[1]
            await StateMachine.task_menu_student.set()
            await TaskMenuState.prepare(message)


async def prepare(message: types.Message):
    keyboard = await Keyboards().create_CHOOSE_TASK_KEYBOARD(stateInfoHolder.get(message.from_user.id).user_id)
    await message.reply("Выберите действие:", reply_markup=keyboard)
