from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.controller.States import HelpMenu, State, StudentMenu, TeacherMenu, WaitAuth
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.UserRepository import UserRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(WaitAuth)
class WaitAuthStateController(Controller):
    def __init__(
        self,
        state_info_repository: StateInfoRepository,
        user_repository: UserRepository,
    ):
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.user_repository: UserRepository = user_repository

    ENTER_LOGIN_PLEASE = "Введите свой токен, или нажмите 'Назад'"
    SUCCESS_AUTH_TEACHER = "Вы успешно авторизованы как преподаватель!"
    SUCCESS_AUTH_STUDENT = "Вы успешно авторизованы как ученик!"
    INCORRECT_CODE = "Пользователя с таким токеном не существует, попробуйте еще раз.\n"
    BACK = "◂ Назад"

    BACK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BACK))

    async def handle(self, message: types.Message) -> State:

        if message.text == self.BACK:
            return HelpMenu

        user = await self.user_repository.get_by_user_id(message.text)

        if user is None:
            await message.answer(
                self.INCORRECT_CODE, reply_markup=types.ReplyKeyboardRemove()
            )
            return WaitAuth

        if user.role == "student":
            await message.answer(self.SUCCESS_AUTH_STUDENT)
            self.state_info_repository.create(message.from_user.id, message.text)
            return StudentMenu

        if user.role == "teacher":
            await message.answer(self.SUCCESS_AUTH_TEACHER)
            self.state_info_repository.create(message.from_user.id, message.text)
            return TeacherMenu

    async def prepare(self, message: types.Message):
        await message.answer(self.ENTER_LOGIN_PLEASE, reply_markup=self.BACK_KEYBOARD)
