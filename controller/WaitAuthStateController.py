from aiogram import types

from controller.States import State, StudentMenu, TeacherMenu, WaitAuth
from repository.StateInfoRepository import StateInfoRepository
from repository.UserRepository import UserRepository
from teletrik.Controller import Controller
from teletrik.DI import controller


@controller(WaitAuth)
class WaitAuthStateController(Controller):

    def __init__(self, state_info_repository: StateInfoRepository, user_repository: UserRepository):
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.user_repository: UserRepository = user_repository

    SUCCESS_AUTH_TEACHER = "Вы успешно авторизованы как преподаватель!"
    SUCCESS_AUTH_STUDENT = "Вы успешно авторизованы как ученик!"
    INCORRECT_CODE = "Пользователя с таким логином не существует, попробуйте еще раз.\n" \
                     + "Проверьте правильность написания логина (`student` и `Student` — два разных логина)"

    async def handle(self, message: types.Message) -> State:

        user = await self.user_repository.get_user(message.text)

        if user is None:
            await message.answer(self.INCORRECT_CODE, reply_markup=types.ReplyKeyboardRemove())
            return

        if user.role == "student":
            await message.answer(self.SUCCESS_AUTH_STUDENT)
            self.state_info_repository.create(message.from_user.id, message.text)
            return StudentMenu

        if user.role == "teacher":
            await message.answer(self.SUCCESS_AUTH_TEACHER)
            self.state_info_repository.create(message.from_user.id, message.text)
            return TeacherMenu

    async def prepare(self, message: types.Message):
        pass
