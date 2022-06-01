from aiogram.types import KeyboardButton, Message, ParseMode, ReplyKeyboardMarkup
import aiogram.utils.markdown as md
from bot.controller.States import StudentMenu, SubmitTask, TaskMenu
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.service.LektoriumService import LektoriumService
from bot.teletrik.Controller import Controller
from bot.teletrik.DI import controller
from bot.view.SubmitView import SubmitView


@controller(TaskMenu)
class TaskMenuStateController(Controller):
    def __init__(
        self,
        task_repository: TaskRepository,
        submit_repository: SubmitRepository,
        state_info_repository: StateInfoRepository,
        lektorium_service: LektoriumService,
        submit_view: SubmitView
    ):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.lektorium_service: LektoriumService = lektorium_service
        self.submit_view: SubmitView = submit_view

    STATEMENT = "Условие"
    SUBMIT_RESULTS = "Попытки"
    DATA_FOR_LEKTORIUM = "Данные для Лекториума"
    SUBMIT = "Отправить ▸"
    BACK = "◂ Назад"

    CHOOSE_ACTION = "Выберите действие"

    TASK_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
    TASK_MENU_KEYBOARD.add(KeyboardButton(SUBMIT))
    TASK_MENU_KEYBOARD.add(KeyboardButton(SUBMIT_RESULTS))
    TASK_MENU_KEYBOARD.add(KeyboardButton(DATA_FOR_LEKTORIUM))
    TASK_MENU_KEYBOARD.add(KeyboardButton(STATEMENT))
    TASK_MENU_KEYBOARD.add(KeyboardButton(BACK))

    async def handle(self, message: Message):

        match message.text:

            case self.STATEMENT:
                task_name = self.state_info_repository.get(
                    message.from_user.id
                ).chosen_task
                tasks = self.task_repository.get_tasks()
                for task in tasks.keys():
                    if task == task_name:
                        await message.answer(text=tasks[task])
                return TaskMenu

            case self.SUBMIT_RESULTS:
                state_info = self.state_info_repository.get(message.from_user.id)
                results = await self.submit_view.get_student_submits_view(
                    state_info.user_id, state_info.chosen_task
                )
                await message.answer(
                    md.code(results),
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=self.TASK_MENU_KEYBOARD,
                )
                return TaskMenu

            case self.SUBMIT:
                return SubmitTask

            case self.BACK:
                return StudentMenu

            case self.DATA_FOR_LEKTORIUM:
                tg_id = message.from_user.id
                user_info = self.state_info_repository.get(tg_id)
                result = await self.lektorium_service.get_task_info(
                    user_info.chosen_task, user_info.user_id
                )
                match result:
                    case self.lektorium_service.NO_POSITIVE_SUBMIT:
                        await message.answer(
                            "Вы не можете получить данные для Лекториума, так как не сдали задачу"
                        )
                    case self.lektorium_service.GRADING_ERROR:
                        await message.answer(
                            "Сервер проверки сейчас недоступен, попробуйте позже"
                        )
                    case _:
                        await message.answer(
                            f"hash: {result['hash']}\npin: {result['pin']}"
                        )
                return TaskMenu

            case _:
                await message.answer(
                    "Я Вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return TaskMenu

    async def prepare(self, message: Message):
        await message.answer(self.CHOOSE_ACTION, reply_markup=self.TASK_MENU_KEYBOARD)
