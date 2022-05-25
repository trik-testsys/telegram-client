from aiogram.types import Message

from bot.controller.States import WaitAuth, Register

from bot.repository.UserRepository import UserRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller, Command, State


@controller(Command)
class CommandController(Controller):

    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    async def handle(self, message: Message) -> State:

        match message.text:

            case "/start":
                return WaitAuth

            case "/register":
                return Register

    async def prepare(self, message: Message):
        pass
