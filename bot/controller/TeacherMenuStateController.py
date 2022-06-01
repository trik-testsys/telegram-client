from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.controller.States import ChoseStudent, TeacherMenu
from bot.repository.SubmitRepository import SubmitRepository
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller
from bot.view.SubmitView import SubmitView


@controller(TeacherMenu)
class TeacherMenuStateController(Controller):
    RESULTS = "Сводная статистика"
    FULL_RESULTS = "Полная статистика"
    CHOOSE_STUDENT = "Ученики ▸"
    UNKNOWN_COMMAND = "Неизвестная команда"
    BACK = "◂ Назад"
    CHOOSE_ACTION = "Выберите действие"

    TEACHER_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(RESULTS),
        KeyboardButton(FULL_RESULTS),
        KeyboardButton(CHOOSE_STUDENT),
    )

    def __init__(self,
                 submit_repository: SubmitRepository,
                 submit_view: SubmitView):
        self.submit_repository: SubmitRepository = submit_repository
        self.submit_view: SubmitView = submit_view

    async def handle(self, message: types.Message):
        match message.text:

            case self.RESULTS:
                results = await self.submit_view.get_stat_view()
                await message.answer(results, reply_markup=self.TEACHER_MENU_KEYBOARD)
                return TeacherMenu

            case self.FULL_RESULTS:
                results = await self.submit_view.get_all_results_view()
                await message.bot.send_document(
                    message.from_user.id, ("results.html", results)
                )
                await message.answer(
                    "Результаты", reply_markup=self.TEACHER_MENU_KEYBOARD
                )
                return TeacherMenu

            case self.CHOOSE_STUDENT:
                return ChoseStudent

            case _:
                await message.answer(
                    "Я вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return TeacherMenu

    async def prepare(self, message: types.Message):
        await message.reply(self.CHOOSE_ACTION, reply_markup=self.TEACHER_MENU_KEYBOARD)
