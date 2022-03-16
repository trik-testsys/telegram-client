from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.controller.StateController.States import States
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.loader import dp
import aiogram.utils.markdown as md

from utils.injector import StateController, ChangeState


@StateController(States.task_menu_student, dp)
class TaskMenuStateController:

    taskRepository = TaskRepository
    submitRepository = SubmitRepository
    stateInfoRepository = StateInfoRepository

    STATEMENT = "Условие"
    SUBMIT_RESULTS = "Попытки"
    SUBMIT = "Отправить ▸"
    BACK = "◂ Назад"

    CHOOSE_ACTION = "Выберите действие"

    TASK_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
    TASK_MENU_KEYBOARD.add(KeyboardButton(SUBMIT))
    TASK_MENU_KEYBOARD.add(KeyboardButton(SUBMIT_RESULTS))
    TASK_MENU_KEYBOARD.add(KeyboardButton(STATEMENT))
    TASK_MENU_KEYBOARD.add(KeyboardButton(BACK))

    @classmethod
    async def handler(cls, message: types.Message):

        match message.text:

            case cls.STATEMENT:
                task_name = cls.stateInfoRepository.get(message.from_user.id).chosen_task
                tasks = cls.taskRepository.get_tasks()
                for task in tasks.keys():
                    if task == task_name:
                        await message.answer(text=tasks[task])

            case cls.SUBMIT_RESULTS:
                state_info = cls.stateInfoRepository.get(message.from_user.id)
                results = await cls.submitRepository.get_student_submits_view(state_info.user_id, state_info.chosen_task)
                await message.answer(md.code(results), parse_mode=ParseMode.MARKDOWN_V2,
                                     reply_markup=cls.TASK_MENU_KEYBOARD)

            case cls.SUBMIT:
                await ChangeState(States.submit, message)

            case cls.BACK:
                await ChangeState(States.student_menu, message)

            case _:
                await message.answer("Я Вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.answer(cls.CHOOSE_ACTION, reply_markup=cls.TASK_MENU_KEYBOARD)
