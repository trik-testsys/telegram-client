from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.controller.States import HelpMenu, StudentMenu, TaskMenu
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

    def __init__(
        self,
        task_repository: TaskRepository,
        submit_repository: SubmitRepository,
        state_info_repository: StateInfoRepository,
    ):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository

    async def create_CHOOSE_TASK_KEYBOARD(self, student):
        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await self.submit_repository.get_student_result(student)

        for task_name in sorted(results.keys()):
            result = results[task_name]
            CHOOSE_TASK_KEYBOARD.add(
                KeyboardButton(f" {task_name} | {self.new_result_view(result)} ▸")
            )

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(self.UPDATE))
        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(self.HELP))
        return CHOOSE_TASK_KEYBOARD

    async def handle(self, message: types.Message) -> State:
        match message.text:

            case self.UPDATE:
                keyboard = await self.create_CHOOSE_TASK_KEYBOARD(
                    self.state_info_repository.get(message.from_user.id).user_id
                )
                await message.answer("Обновлено", reply_markup=keyboard)
                return StudentMenu

            case self.HELP:
                return HelpMenu

            case _:
                info = message.text.split()
                if len(info) < 2:
                    await message.answer(
                        "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                    )
                    return StudentMenu
                if info[0] in self.task_repository.get_tasks():
                    self.state_info_repository.get(
                        message.from_user.id
                    ).chosen_task = info[0]
                    return TaskMenu
                await message.answer(
                    "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return StudentMenu

    async def prepare(self, message: types.Message):
        keyboard = await self.create_CHOOSE_TASK_KEYBOARD(
            self.state_info_repository.get(message.from_user.id).user_id
        )
        await message.answer(self.CHOOSE_ACTION, reply_markup=keyboard)

    def new_result_view(self, res: str) -> str:

        match res[0]:

            case "+":
                return res.replace("+", "✅ | Попыток: ")
            case "-":
                return res.replace("-", "❌ | Попыток: ")
            case "?":
                return res.replace("?", "🔄 | Попыток: ")
            case "0":
                return res.replace("0", " Попыток: 0")
