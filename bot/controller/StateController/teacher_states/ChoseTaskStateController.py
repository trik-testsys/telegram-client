from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.controller.StateController.States import States
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository


from bot.loader import dp
from utils.injector import StateController, ChangeState


@StateController(States.chose_task, dp)
class ChoseTaskStateController:

    taskRepository = TaskRepository
    submitRepository = SubmitRepository
    stateInfoRepository = StateInfoRepository

    RESULTS = "Результаты"
    CHOOSE_TASK = "Задачи ученика ▸"
    BACK = "◂ Назад"

    @classmethod
    async def create_CHOOSE_TASK_KEYBOARD(cls, message):

        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        student_result = await cls.submitRepository.get_student_result(cls.stateInfoRepository.get(message.from_user.id).chosen_student)
        for task_name in student_result.keys():
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f"Задача: {task_name} Результат: {student_result[task_name]}"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(cls.BACK))
        return CHOOSE_TASK_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):

        if message.text == cls.BACK:
            await ChangeState(States.chose_student, message)
            return

        text = message.text.split()

        if len(text) < 2:
            await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
            return

        task_name = text[1]
        if task_name not in cls.taskRepository.get_tasks():
            await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
            return

        cls.stateInfoRepository.get(message.from_user.id).chosen_task = task_name
        await ChangeState(States.chose_submit, message)

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.answer(cls.CHOOSE_TASK, reply_markup=await cls.create_CHOOSE_TASK_KEYBOARD(message))
