from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.controller.States import HelpMenu, StudentMenu, TaskMenu, TeacherMenu
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.repository.UserRepository import UserRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller, State
from bot.view.SubmitView import SubmitView


@controller(StudentMenu)
class StudentMenuController(Controller):
    UPDATE = "Обновить результаты"
    CHOOSE_ACTION = "Выберите задачу"
    HELP = "Помощь ▸"
    TEACHER_PANEL = "Панель учителя ▸"

    def __init__(
        self,
        task_repository: TaskRepository,
        submit_repository: SubmitRepository,
        state_info_repository: StateInfoRepository,
        user_repository: UserRepository,
        submit_view: SubmitView,
    ):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.user_repository: UserRepository = user_repository
        self.submit_view: SubmitView = submit_view

    async def create_choose_task_keyboard(self, user_id: str) -> ReplyKeyboardMarkup:
        choose_task_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        results = await self.submit_view.get_student_result(user_id)

        for task_name in sorted(results.keys()):
            choose_task_keyboard.add(
                KeyboardButton(f" {task_name} | {results[task_name]} ▸")
            )

        choose_task_keyboard.add(KeyboardButton(self.UPDATE))
        choose_task_keyboard.add(KeyboardButton(self.HELP))

        user = await self.user_repository.get_by_user_id(user_id)
        if user is not None and user.role == "teacher":
            choose_task_keyboard.add(KeyboardButton(self.TEACHER_PANEL))
        return choose_task_keyboard

    async def handle(self, message: types.Message) -> State:
        match message.text:

            case self.UPDATE:
                keyboard = await self.create_choose_task_keyboard(
                    self.state_info_repository.get(message.from_user.id).user_id
                )
                await message.answer("Обновлено", reply_markup=keyboard)
                return StudentMenu

            case self.HELP:
                return HelpMenu

            case self.TEACHER_PANEL:
                user = await self.user_repository.get_by_telegram_id(message.from_user.id)
                if user is not None and user.role == "teacher":
                    return TeacherMenu
                await message.answer(
                    "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return StudentMenu

            case _:
                info = message.text.split(":")
                if len(info) < 2:
                    await message.answer(
                        "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                    )
                    return StudentMenu
                task_id = info[0]
                if self.task_repository.task_exists(task_id):
                    self.state_info_repository.get(
                        message.from_user.id
                    ).chosen_task = task_id
                    return TaskMenu
                await message.answer(
                    "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return StudentMenu

    async def prepare(self, message: types.Message):
        keyboard = await self.create_choose_task_keyboard(
            self.state_info_repository.get(message.from_user.id).user_id,
        )
        await message.answer(self.CHOOSE_ACTION, reply_markup=keyboard)
