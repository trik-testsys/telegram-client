from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.Controller.StateController.States import States
from bot.Repository.TaskRepository import TaskRepository
from bot.data.Submit import get_student_result


from bot.loader import stateInfoHolder,  dp
from bot.utils.injector import StateController, ChangeState, Autowired


@StateController(States.chose_task, dp)
class ChoseTaskStateController:

    taskRepository = TaskRepository

    RESULTS = "Результаты"
    CHOOSE_TASK = "Задачи ученика"
    BACK = "Назад"

    @classmethod
    async def create_CHOOSE_TASK_KEYBOARD(cls, message):

        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        student_result = await get_student_result(stateInfoHolder.get(message.from_user.id).chosen_student)
        for task_name in student_result.keys():
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f"{student_result[task_name]} {task_name}"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(cls.BACK))
        return CHOOSE_TASK_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):

        if message.text == cls.BACK:
            await ChangeState(States.chose_student, message)
            return

        text = message.text.split()

        if len(text) != 2:
            return

        task_name = text[1]
        if task_name not in cls.taskRepository.get_tasks():
            return

        stateInfoHolder.get(message.from_user.id).chosen_task = task_name
        await ChangeState(States.chose_submit, message)

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.answer(cls.CHOOSE_TASK, reply_markup=await cls.create_CHOOSE_TASK_KEYBOARD(message))
