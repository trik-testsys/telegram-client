from typing import List

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from bot.controller.States import ChoseStudent, ChoseTask, TeacherMenu
from bot.model.User import User
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.UserRepository import UserRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller, State


@controller(ChoseStudent)
class ChoseStudentStateController(Controller):
    def __init__(
        self,
        state_info_repository: StateInfoRepository,
        user_repository: UserRepository,
    ) -> None:
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.user_repository: UserRepository = user_repository

    RESULTS = "Результаты"
    FULL_STAT = "Полная статистика"
    CHOOSE_STUDENT = "Ученики ▸"
    BACK = "◂ Назад"

    async def handle(self, message: Message) -> State:

        if message.text == self.BACK:
            return TeacherMenu

        if await self._validate_message(message):
            self.state_info_repository.get(
                message.from_user.id
            ).chosen_student = self._get_id(message)
            return ChoseTask
        else:
            await message.answer(
                "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
            )
            return ChoseStudent

    async def prepare(self, message: Message):
        await message.answer(
            self.CHOOSE_STUDENT, reply_markup=await self._get_chose_student_keyboard()
        )

    async def _validate_message(self, message: Message) -> bool:
        text: List[str] = message.text.split()
        return len(text) == 2 and await self._is_student(self._get_id(message))

    @staticmethod
    def _get_id(message: Message) -> str:
        return message.text.split()[0]

    async def _get_chose_student_keyboard(self) -> ReplyKeyboardMarkup:
        choose_student_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        for student in await self.user_repository.get_by_role("student"):
            choose_student_keyboard.add(KeyboardButton(f"{student} ▸"))
        choose_student_keyboard.add(KeyboardButton(self.BACK))
        return choose_student_keyboard

    async def _is_student(self, user_id: str):
        user: User = await self.user_repository.get_by_user_id(user_id)
        return user.role == "student"
