from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from bot.controller.States import Cabinet, HelpMenu, WaitAuth
from bot.model.User import User
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.UserRepository import UserRepository
from bot.service.TokenService import TokenService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(Cabinet)
class CabinetController(Controller):

    def __init__(
            self,
            user_repository: UserRepository,
            token_service: TokenService,
            state_info_repository: StateInfoRepository,
    ):
        self.user_repository: UserRepository = user_repository
        self.token_service: TokenService = token_service
        self.state_info_repository: StateInfoRepository = state_info_repository

    BACK = "◂ Назад"
    AUTH = "Сменить кабинет ▸"
    REMEMBER = "Напомнить токен"

    CHOOSE_ACTION = "Выберите действие, нажав нужную кнопку"

    CABINET_MENU_KEYBOARD = ReplyKeyboardMarkup()
    CABINET_MENU_KEYBOARD.add(
        KeyboardButton(AUTH),
        KeyboardButton(REMEMBER),
        KeyboardButton(BACK),
    )

    async def handle(self, message: Message):

        match message.text:

            case self.BACK:
                return HelpMenu

            case self.AUTH:
                return WaitAuth

            case self.REMEMBER:
                tg_id: str = message.from_user.id
                user: User | None = await self.user_repository.get_by_telegram_id(tg_id)

                if user is None:
                    await message.answer(
                        "Вы ещё не зарегестрированы, для регистрации отправьте /start"
                    )
                else:
                    await message.answer("Ваш токен:")
                    await message.answer(user.user_id)
                return Cabinet

            case _:
                await message.answer(
                    "Я Вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return Cabinet

    async def prepare(self, message: Message):
        await message.answer(self.CHOOSE_ACTION, reply_markup=self.CABINET_MENU_KEYBOARD)
