from aiogram import types
from aiogram.types import KeyboardButton, ParseMode, ReplyKeyboardMarkup
from bot.controller.States import Cabinet, HelpMenu, StudentMenu
from bot.model.User import User
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.UserRepository import UserRepository
from bot.service.TokenService import TokenService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller


@controller(HelpMenu)
class HelpMenuStateController(Controller):
    def __init__(
        self,
        user_repository: UserRepository,
        token_service: TokenService,
        state_info_repository: StateInfoRepository,
    ):
        self.user_repository: UserRepository = user_repository
        self.token_service: TokenService = token_service
        self.state_info_repository: StateInfoRepository = state_info_repository

    MAIN_MENU = "◂ Главное меню"
    HOW_TO_CHECK_TASK = "ℹ Как устроена проверка задач?"
    HOW_TO_UNDERSTAND_RESULTS = "ℹ️ Что означают + - ? ✅ ❌ 🔄"
    HOW_TO_CABINET = "Настройки кабинета ▸"

    CHOOSE_ACTION = "Выберите действие, нажав нужную кнопку"

    HELP_MENU_KEYBOARD = ReplyKeyboardMarkup()
    HELP_MENU_KEYBOARD.add(
        KeyboardButton(HOW_TO_CHECK_TASK),
        KeyboardButton(HOW_TO_UNDERSTAND_RESULTS),
        KeyboardButton(MAIN_MENU),
        KeyboardButton(HOW_TO_CABINET)
    )

    async def handle(self, message: types.Message):

        match message.text:

            case self.MAIN_MENU:
                tg_id: str = message.from_user.id
                user: User | None = await self.user_repository.get_by_telegram_id(tg_id)

                if user is None:
                    token: str = self.token_service.generate_new_token(tg_id)
                    await self.user_repository.create_user(token, "student", tg_id)
                    self.state_info_repository.create(message.from_user.id, token)
                    return StudentMenu
                else:
                    self.state_info_repository.create(
                        message.from_user.id, user.user_id
                    )
                    return StudentMenu

            case self.HOW_TO_CABINET:
                return Cabinet

            case self.HOW_TO_CHECK_TASK:
                await message.answer(
                    """*Как устроена проверка задач*
1. Выберите задачу в меню
2. Прикрепите файл с решением и отправьте его. Бот начнёт обработку. Обычно это занимает не более 10 минут.
3. Таблицу с результатами обработки можно посмотреть в меню "Результаты запусков"
4. Если запуск был удачный, то в меню "Лучший результат" вы получите пин-код и хеш, которые надо использовать на курсе.""",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return HelpMenu
            case self.HOW_TO_UNDERSTAND_RESULTS:
                await message.answer(
                    """*Статусы решений*
⚬ `+` — решение правильное.
⚬ `-` — решение неправильное.
⚬ `?` — решение тестируется.
*Статусы задач*
Если было отправлено хотя бы одно решение, вы сможете увидеть один из следующих статусов:
⚬ ✅ — если было отправлено хотя бы одно правильное решение.
⚬ ❌ — если правильных решений нет.
⚬ 🔄 — если правильных решений нет, но есть решения, которые тестируются.""",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return HelpMenu
            case _:
                await message.answer(
                    "Я Вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return HelpMenu

    async def prepare(self, message: types.Message):
        await message.answer(self.CHOOSE_ACTION, reply_markup=self.HELP_MENU_KEYBOARD)
