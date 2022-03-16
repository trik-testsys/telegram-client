import logging

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.injector import ChangeState, StateController

from bot.controller.StateController.States import States
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.loader import dp


@StateController(States.student_menu, dp)
class StudentMenuController:
    taskRepository = TaskRepository
    submitRepository = SubmitRepository
    stateInfoRepository = StateInfoRepository

    UPDATE = "Обновить результаты"
    CHOOSE_ACTION = "Выберите задачу"
    FEEDBACK = "Поддержка"

    @classmethod
    async def create_CHOOSE_TASK_KEYBOARD(cls, student):
        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await cls.submitRepository.get_student_result(student)

        for task_name in sorted(results.keys()):
            result = results[task_name]
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f" {task_name} | {cls.new_result_view(result)} ▸"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(cls.UPDATE))

        return CHOOSE_TASK_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):
        match message.text:

            case cls.UPDATE:
                await cls.prepare(message)

            case _:
                info = message.text.split()
                if len(info) < 2:
                    await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
                    return
                if info[0] in cls.taskRepository.get_tasks():
                    cls.stateInfoRepository.get(message.from_user.id).chosen_task = info[0]
                    await ChangeState(States.task_menu_student, message)
                    return
                await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")

    @classmethod
    async def prepare(cls, message: types.Message):
        keyboard = await cls.create_CHOOSE_TASK_KEYBOARD(cls.stateInfoRepository.get(message.from_user.id).user_id)
        await message.answer(cls.CHOOSE_ACTION, reply_markup=keyboard)

    @classmethod
    def new_result_view(cls, res: str) -> str:

        match res[0]:

            case '+':
                return res.replace("+", "✅ | Попыток: ")
            case '-':
                return res.replace("-", "❌ | Попыток: ")
            case '?':
                return res.replace("?", "🔄 | Попыток: ")
            case '0':
                return res.replace("0", " Попыток: 0")
