from aiogram.types import KeyboardButton, Message, ParseMode, ReplyKeyboardMarkup
import aiogram.utils.markdown as md
from bot.controller.States import StudentMenu, TaskMenu
from bot.repository.StateInfoRepository import StateInfoRepository
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.TaskRepository import TaskRepository
from bot.service.GradingService import GradingService
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
        submit_view: SubmitView,
        grading_service: GradingService,
    ):
        self.task_repository: TaskRepository = task_repository
        self.submit_repository: SubmitRepository = submit_repository
        self.state_info_repository: StateInfoRepository = state_info_repository
        self.lektorium_service: LektoriumService = lektorium_service
        self.submit_view: SubmitView = submit_view
        self.grading_service: GradingService = grading_service

    SUBMIT_RESULTS = "Результаты запусков"
    DATA_FOR_LEKTORIUM = "Лучший результат"
    BACK = "◂ Назад"
    SENT = "Бот принял вашу работу и начал её анализировать. Таблицу с результатами обработки можно посмотреть в меню 'Результаты запусков'"
    NOT_SENT = (
        "Решение не отправлено так как сервер проверки недоступен. Попробуйте позже"
    )
    ERROR_NOT_FILE = "Пожалуйста, отправьте файл"

    async def handle(self, message: Message):

        is_submit: bool = await self.handle_submit(message)
        if is_submit:
            return TaskMenu

        match message.text:

            case self.SUBMIT_RESULTS:
                state_info = self.state_info_repository.get(message.from_user.id)
                results = await self.submit_view.get_student_submits_view(
                    state_info.user_id, state_info.chosen_task
                )
                await message.answer(
                    md.code(results),
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=await self._create_keyboard(message)
                )
                return TaskMenu

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
                            "Система выбрала лучший удачный результат из отправленных вами. Чтобы засчитать этот результат скопируйте данные ниже в форму на Лекториуме:"
                        )
                        await message.answer(f"Пин-код: {result['pin']}")
                        await message.answer(f"Проверочный код {result['hash']}")
                return TaskMenu

            case _:
                await message.answer(
                    "Я Вас не понял, пожалуйста воспользуйтесь кнопкой из клавиатуры"
                )
                return TaskMenu

    async def handle_submit(self, message: Message) -> bool:

        if message.document is None:
            return False

        document_id = message.document.file_id
        file = await message.bot.download_file_by_id(document_id)
        state_info = self.state_info_repository.get(message.from_user.id)
        submit_id = await self.grading_service.send_task(
            state_info.chosen_task, state_info.user_id, file
        )

        if submit_id != self.grading_service.ERROR:
            await message.answer(f"{self.SENT}, ID решения: {submit_id}")
        else:
            await message.answer(f"{self.NOT_SENT}")
        return True

    async def prepare(self, message: Message):
        await message.answer(
            await self._get_description(message),
            reply_markup=await self._create_keyboard(message),
        )

    async def _create_keyboard(self, message: Message) -> ReplyKeyboardMarkup:
        task_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        task_menu_keyboard.add(KeyboardButton(self.SUBMIT_RESULTS))

        tg_id = message.from_user.id
        user_info = self.state_info_repository.get(tg_id)
        result = await self.lektorium_service.get_task_info(
            user_info.chosen_task, user_info.user_id
        )
        if result != self.lektorium_service.NO_POSITIVE_SUBMIT:
            task_menu_keyboard.add(KeyboardButton(self.DATA_FOR_LEKTORIUM))

        task_menu_keyboard.add(KeyboardButton(self.BACK))
        return task_menu_keyboard

    async def _get_description(self, message: Message) -> str:
        task_name = self.state_info_repository.get(message.from_user.id).chosen_task
        tasks = self.task_repository.get_tasks()
        for task in tasks.keys():
            if task == task_name:
                return f"Задача: {task}\nОписание: {tasks[task]}"
