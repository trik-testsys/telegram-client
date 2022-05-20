from aiogram.types import Message

from bot.controller.States import WaitAuth
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller, Command, State


@controller(Command)
class CommandController(Controller):

    def __init__(self):
        pass

    async def handle(self, message: Message) -> State:

        match message.text:

            case "/start":
                return WaitAuth

    async def prepare(self, message: Message):
        pass
