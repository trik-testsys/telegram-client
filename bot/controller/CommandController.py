from aiogram.types import Message
from bot.controller.States import HelpMenu, StudentMenu
from bot.model.User import User
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.UserRepository import UserRepository
from bot.service.TokenService import TokenService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import Command, controller, State


@controller(Command)
class CommandController(Controller):
    def __init__(
        self,
        user_repository: UserRepository,
        token_service: TokenService,
        state_info_repository: StateInfoRepository,
    ):
        self.user_repository: UserRepository = user_repository
        self.token_service: TokenService = token_service
        self.state_info_repository: StateInfoRepository = state_info_repository

    async def handle(self, message: Message) -> State:

        match message.text:

            case "/start":
                tg_id: str = message.from_user.id
                user: User | None = await self.user_repository.get_by_telegram_id(tg_id)

                if user is None:
                    token: str = self.token_service.generate_new_token(tg_id)
                    await self.user_repository.create_user(token, "student", tg_id)
                    self.state_info_repository.create(message.from_user.id, token)
                else:
                    self.state_info_repository.create(
                        message.from_user.id, user.user_id
                    )
                return StudentMenu

            case "/help":
                return HelpMenu

    async def prepare(self, message: Message):
        pass
