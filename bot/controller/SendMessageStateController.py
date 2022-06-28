from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.controller.States import TeacherMenu, SendMessage
from bot.repository.UserRepository import UserRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(SendMessage)
class SendMessageStateController(Controller):
    def __init__(self, user_repository: UserRepository,):
        self.user_repository: UserRepository = user_repository

    BACK = "◂ Назад"
    CHOOSE_ACTION = "Отправьте сообщение для рассылки, или нажмите '◂ Назад'"

    HELP_MENU_KEYBOARD = ReplyKeyboardMarkup()
    HELP_MENU_KEYBOARD.add(
        KeyboardButton(BACK)
    )

    async def handle(self, message: types.Message):

        match message.text:

            case self.BACK:
                return TeacherMenu

            case _:
                for user in await self.user_repository.get_all_students():
                    await message.bot.send_message(chat_id=user.telegram_id, text=f"Информация:\n{message.text}")
                await message.answer("Сообщение успешно отправлено! "
                                     "Отправьте еще одно сообщение, или нажмите '◂ Назад'")
                return SendMessage

    async def prepare(self, message: types.Message):
        await message.answer(self.CHOOSE_ACTION, reply_markup=self.HELP_MENU_KEYBOARD)