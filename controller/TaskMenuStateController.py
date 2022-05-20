from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from controller.States import TaskMenu, SubmitTask, StudentMenu
from repository.StateInfoRepository import StateInfoRepository
from repository.SubmitRepository import SubmitRepository
from repository.TaskRepository import TaskRepository

import aiogram.utils.markdown as md

from teletrik.Controller import Controller
from teletrik.DI import controller


@controller(TaskMenu)
class TaskMenuStateController(Controller):

    def __init__(self,
                 task_repository: TaskRepository,
                 submit_repository: SubmitRepository,
                 state_info_repository: StateInfoRepository):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository

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

    async def handle(self, message: types.Message):

        match message.text:

            case self.STATEMENT:
                task_name = self.state_info_repository.get(message.from_user.id).chosen_task
                tasks = self.task_repository.get_tasks()
                for task in tasks.keys():
                    if task == task_name:
                        await message.answer(text=tasks[task])
                return TaskMenu

            case self.SUBMIT_RESULTS:
                state_info = self.state_info_repository.get(message.from_user.id)
                results = await self.submit_repository.get_student_submits_view(state_info.user_id,
                                                                                state_info.chosen_task)
                await message.answer(md.code(results), parse_mode=ParseMode.MARKDOWN_V2,
                                     reply_markup=self.TASK_MENU_KEYBOARD)
                return TaskMenu

            case self.SUBMIT:
                return SubmitTask

            case self.BACK:
                return StudentMenu

            case _:
                await message.answer("Я Вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
                return TaskMenu

    async def prepare(self, message: types.Message):
        await message.answer(self.CHOOSE_ACTION, reply_markup=self.TASK_MENU_KEYBOARD)
