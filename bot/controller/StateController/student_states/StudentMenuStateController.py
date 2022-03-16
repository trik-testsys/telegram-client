import logging

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from utils.injector import ChangeState, StateController
import aiogram.utils.markdown as md

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
    HELP = "Помощь"
    HELP_MESSAGE = \
f"""
*Как сдать задачу?*
 1. В появившемся после авторизации меню нажмите на кнопку с задачей, решение на которую собираетесь отправить.
 2. Нажмите на `Отправить▸`.
 3. Прикрепите файл с решением и отправьте его боту.
 4. В ответ вы получите id вашего решения, по которому вы сможете узнать результат.
    
*Как узнать результат?*
 1. В появившемся после авторизации меню вы можете увидеть итоговый результат по каждой задаче (подробнее в `Статусы задач`).
 2. Если вы хотите узнать результат по конкретному решению, то нажмите на кнопку с соответсвующей задачей.
 3. Нажмите на `Попытки`.
 4. В ответ вы получите таблицу с результатом проверки по каждому отправленному решению (подробнее в `Статусы решений`).
    
*Статусы задач*
Если было отправлено хотя бы одно решение, вы сможете увидеть один из следующих статусов:
 ⚬ ✅ — если было отправлено хотя бы одно правильное решение.
 ⚬ ❌ — если правильных решений нет.
 ⚬ 🔄 — если правильных решений нет, но есть решения, которые тестируются.
     
*Статусы решений*
 ⚬ `+` — решение правильное.
 ⚬ `-` — решение неправильное.
 ⚬ `?` — решение тестируется.
"""

    @classmethod
    async def create_CHOOSE_TASK_KEYBOARD(cls, student):
        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await cls.submitRepository.get_student_result(student)

        for task_name in sorted(results.keys()):
            result = results[task_name]
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f" {task_name} | {cls.new_result_view(result)} ▸"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(cls.UPDATE))
        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(cls.HELP))
        return CHOOSE_TASK_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):
        match message.text:

            case cls.UPDATE:
                await cls.prepare(message)

            case cls.HELP:
                await message.answer(text=cls.HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)

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
