from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from bot.controller.States import ChoseStudent, ChoseSubmit, ChoseTask
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller
from bot.view.SubmitView import SubmitView


@controller(ChoseTask)
class ChoseTaskStateController(Controller):
    def __init__(
        self,
        task_repository: TaskRepository,
        submit_repository: SubmitRepository,
        state_info_repository: StateInfoRepository,
        submit_view: SubmitView,
    ):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.submit_view: SubmitView = submit_view

    RESULTS = "Результаты"
    CHOOSE_TASK = "Задачи ученика ▸"
    BACK = "◂ Назад"

    async def create_choose_task_keyboard(self, message):

        choose_task_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        student_result = await self.submit_view.get_student_result(
            self.state_info_repository.get(message.from_user.id).chosen_student
        )
        for task_name in student_result.keys():
            choose_task_keyboard.add(
                KeyboardButton(f"{task_name} {student_result[task_name]} ▸")
            )

        choose_task_keyboard.add(KeyboardButton(self.BACK))
        return choose_task_keyboard

    async def handle(self, message: Message):
        if not self._validate_message(message):
            await message.answer(
                "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
            )
            return ChoseTask

        if message.text == self.BACK:
            return ChoseStudent

        task_name: str = self._get_task_name(message)
        self.state_info_repository.get(message.from_user.id).chosen_task = task_name
        return ChoseSubmit

    async def prepare(self, message: Message):
        await message.answer(
            self.CHOOSE_TASK,
            reply_markup=await self.create_CHOOSE_TASK_KEYBOARD(message),
        )

    def _validate_message(self, message: Message) -> bool:
        text: list[str] = message.text.split()
        if len(text) < 2:
            return False
        task_name: str = text[0]
        return task_name not in self.task_repository.get_tasks()

    @staticmethod
    def _get_task_name(message: Message) -> str:
        text: list[str] = message.text.split()
        return text[0]
