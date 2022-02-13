from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.Controller.StateController.States import States
from bot.Repository.TaskRepository import TaskRepository
from bot.data.Submit import get_student_result
from bot.loader import stateInfoHolder, dp
from bot.utils.injector import ChangeState, StateController


@StateController(States.student_menu, dp)
class StudentMenuController:

    taskRepository = TaskRepository

    UPDATE = "Обновить"

    CHOOSE_ACTION = "Выберите действие"

    @classmethod
    async def create_CHOOSE_TASK_KEYBOARD(cls, student):
        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await get_student_result(student)

        for task_name in results.keys():
            result = results[task_name]
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f"{result} {task_name}"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(cls.UPDATE))

        return CHOOSE_TASK_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):
        match message.text:

            case cls.UPDATE:
                await cls.prepare(message)

            case _:
                info = message.text.split()
                if len(info) != 2:
                    return
                if info[1] in cls.taskRepository.get_tasks():
                    stateInfoHolder.get(message.from_user.id).chosen_task = info[1]

                await ChangeState(States.task_menu_student, message)

    @classmethod
    async def prepare(cls, message: types.Message):
        keyboard = await cls.create_CHOOSE_TASK_KEYBOARD(stateInfoHolder.get(message.from_user.id).user_id)
        await message.reply("Выберите действие:", reply_markup=keyboard)
