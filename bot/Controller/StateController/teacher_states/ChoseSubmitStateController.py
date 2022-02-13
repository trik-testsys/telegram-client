from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.Controller.StateController.States import States
from bot.Controller.StateController.teacher_states import ChoseTaskStateController
from bot.data.Submit import get_student_submits_by_task

from bot.grading.GradingClient import get_submit
from bot.loader import stateInfoHolder, bot, dp
from bot.utils.injector import StateController, ChangeState


@StateController(States.chose_submit, dp)
class ChoseSubmitStateController:

    RESULTS = "Результаты"
    CHOOSE_SUBMIT = "Посылки по задаче"
    BACK = "Назад"

    SUBMIT = "Посылка ученика"

    @classmethod
    async def create_CHOOSE_SUBMIT_KEYBOARD(cls, message):
        CHOOSE_SUBMIT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
        state_info = stateInfoHolder.get(message.from_user.id)
        submits = await get_student_submits_by_task(state_info.chosen_student, state_info.chosen_task)
        for submit in submits:
            CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(f"{submit.result} {submit.submit_id}"))

        CHOOSE_SUBMIT_KEYBOARD.add(KeyboardButton(cls.BACK))
        return CHOOSE_SUBMIT_KEYBOARD

    @classmethod
    async def handler(cls, message: types.Message):

        if message.text == cls.BACK:
            await ChangeState(States.chose_submit, message)
            return

        text = message.text.split()

        if len(text) != 2:
            return

        submit_id = text[1]
        await message.answer(cls.SUBMIT)
        file = await get_submit(submit_id)
        await bot.send_document(message.from_user.id, (f'submit_{submit_id}.qrs', file))

    @classmethod
    async def prepare(cls, message: types.Message):
        await message.answer(cls.CHOOSE_SUBMIT, reply_markup=await cls.create_CHOOSE_SUBMIT_KEYBOARD(message))
