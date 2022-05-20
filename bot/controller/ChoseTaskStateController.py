from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

from bot.controller.States import ChoseTask, ChoseStudent, ChoseSubmit
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(ChoseTask)
class ChoseTaskStateController(Controller):

    def __init__(self,
                 task_repository: TaskRepository,
                 submit_repository: SubmitRepository,
                 state_info_repository: StateInfoRepository):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository

    RESULTS = "Результаты"
    CHOOSE_TASK = "Задачи ученика ▸"
    BACK = "◂ Назад"

    async def create_CHOOSE_TASK_KEYBOARD(self, message):

        CHOOSE_TASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        student_result = await self.submit_repository.get_student_result(
            self.state_info_repository.get(message.from_user.id).chosen_student)
        for task_name in student_result.keys():
            CHOOSE_TASK_KEYBOARD.add(KeyboardButton(f"{task_name} {self.new_result_view(student_result[task_name])} ▸"))

        CHOOSE_TASK_KEYBOARD.add(KeyboardButton(self.BACK))
        return CHOOSE_TASK_KEYBOARD

    async def handle(self, message: Message):

        if message.text == self.BACK:
            return ChoseStudent

        text = message.text.split()

        if len(text) < 2:
            await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
            return ChoseTask

        task_name = text[0]
        if task_name not in self.task_repository.get_tasks():
            await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
            return ChoseTask

        self.state_info_repository.get(message.from_user.id).chosen_task = task_name
        return ChoseSubmit

    async def prepare(self, message: Message):
        await message.answer(self.CHOOSE_TASK, reply_markup=await self.create_CHOOSE_TASK_KEYBOARD(message))

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
