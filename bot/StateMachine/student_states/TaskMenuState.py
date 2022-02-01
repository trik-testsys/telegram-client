from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.student_states import StudentMenuState, SubmitState
from bot.data.Submit import get_student_submits_view
from bot.loader import stateInfoHolder, tasks
import aiogram.utils.markdown as md


class Commands:
    STATEMENT = "Условие"
    SUBMIT_RESULTS = "Послыки"
    SUBMIT = "Отправить"
    BACK = "Назад"


class Messages:
    CHOOSE_ACTION = "Выберите действие"


class Keyboards:
    TASK_MENU_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
    TASK_MENU_KEYBOARD.add(KeyboardButton(Commands.STATEMENT))
    TASK_MENU_KEYBOARD.add(KeyboardButton(Commands.SUBMIT_RESULTS))
    TASK_MENU_KEYBOARD.add(KeyboardButton(Commands.SUBMIT))
    TASK_MENU_KEYBOARD.add(KeyboardButton(Commands.BACK))


async def handler(message: types.Message):
    match message.text:

        case Commands.STATEMENT:
            task_name = stateInfoHolder.get(message.from_user.id).chosen_task
            for task in tasks.keys():
                if task == task_name:
                    await message.answer(text=tasks[task])

        case Commands.SUBMIT_RESULTS:
            state_info = stateInfoHolder.get(message.from_user.id)
            results = await get_student_submits_view(state_info.user_id, state_info.chosen_task)
            await message.answer(md.code(results), parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=Keyboards.TASK_MENU_KEYBOARD)

        case Commands.SUBMIT:
            await StateMachine.submit.set()
            await SubmitState.prepare(message)

        case Commands.BACK:
            await StateMachine.student_menu.set()
            await StudentMenuState.prepare(message)


async def prepare(message: types.Message):
    await message.reply(Messages.CHOOSE_ACTION, reply_markup=Keyboards.TASK_MENU_KEYBOARD)
