from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.controller.States import State, Register
from bot.model.User import User
from bot.repository.UserRepository import UserRepository
from bot.service.TokenService import TokenService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(Register)
class WaitAuthStateController(Controller):

    def __init__(self, user_repository: UserRepository, token_service: TokenService):
        self.user_repository: UserRepository = user_repository
        self.token_service: TokenService = token_service

    async def handle(self, message: types.Message) -> State:
        await message.answer("Для авторизации напишите /start")
        return None

    async def prepare(self, message: types.Message):
        tg_id: str = message.from_user.id
        user: User | None = await self.user_repository.get_by_telegram_id(tg_id)

        if user is None:
            token: str = self.token_service.generate_new_token(tg_id)
            await self.user_repository.create_user(token, "student", tg_id)
            await message.answer(f"Успешная регистрация, ваш токен: {token}")
        else:
            await message.answer(f"Вы уже зарегестрированы, ваш токен: {user.user_id}")

