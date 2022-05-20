from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

from controller.States import TeacherMenu, ChoseStudent, ChoseTask
from repository.StateInfoRepository import StateInfoRepository
from repository.UserRepository import UserRepository
from teletrik.Controller import Controller
from teletrik.DI import controller


@controller(ChoseStudent)
class ChoseStudentStateController(Controller):

    def __init__(self, state_info_repository: StateInfoRepository, user_repository: UserRepository):
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.user_repository: UserRepository = user_repository

    RESULTS = "Результаты"
    FULL_STAT = "Полная статистика"
    CHOOSE_STUDENT = "Ученики ▸"
    BACK = "◂ Назад"

    async def handle(self, message: Message):

        if message.text == self.BACK:
            return TeacherMenu

        text = message.text.split()
        if len(text) == 2 and await self.user_repository.is_student(text[0]):
            self.state_info_repository.get(message.from_user.id).chosen_student = text[0]
            return ChoseTask
        else:
            await message.answer("Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры")
            return ChoseStudent

    async def prepare(self, message: Message):
        await message.answer(self.CHOOSE_STUDENT, reply_markup=self._get_chose_student_keyboard())

    def _get_chose_student_keyboard(self) -> ReplyKeyboardMarkup:
        choose_student_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
        for student in self.user_repository.get_all_students():
            choose_student_keyboard.add(KeyboardButton(f"{student} ▸"))
        choose_student_keyboard.add(KeyboardButton(self.BACK))
        return choose_student_keyboard
