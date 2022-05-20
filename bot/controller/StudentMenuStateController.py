from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.controller.States import StudentMenu, TaskMenu
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller, State


@controller(StudentMenu)
class StudentMenuController(Controller):
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

    def __init__(self,
                 task_repository: TaskRepository,
                 submit_repository: SubmitRepository,
                 state_info_repository: StateInfoRepository):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository

    async def create_CHOOSE_TASK_KEYBOARD(self, student):
        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await self.submit_repository.get_student_result(student)

        for task_name in sorted(results.keys()):
            result = results[task_name]
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f" {task_name} | {self.new_result_view(result)} ▸"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(self.UPDATE))
        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(self.HELP))
        return CHOOSE_TASK_KEYBOARD

    async def handle(self, message: types.Message) -> State:
        match message.text:

            case self.UPDATE:
                return StudentMenu

            case self.HELP:
                await message.answer(text=self.HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)
                return StudentMenu

            case _:
                info = message.text.split()
                if len(info) < 2:
                    await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
                    return StudentMenu
                if info[0] in self.task_repository.get_tasks():
                    self.state_info_repository.get(message.from_user.id).chosen_task = info[0]
                    return TaskMenu
                await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
                return StudentMenu

    async def prepare(self, message: types.Message):
        keyboard = await self.create_CHOOSE_TASK_KEYBOARD(self.state_info_repository.get(message.from_user.id).user_id)
        await message.answer(self.CHOOSE_ACTION, reply_markup=keyboard)

    def new_result_view(self, res: str) -> str:

        match res[0]:

            case '+':
                return res.replace("+", "✅ | Попыток: ")
            case '-':
                return res.replace("-", "❌ | Попыток: ")
            case '?':
                return res.replace("?", "🔄 | Попыток: ")
            case '0':
                return res.replace("0", " Попыток: 0")
