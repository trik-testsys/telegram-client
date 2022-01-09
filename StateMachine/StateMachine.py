from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):

    wait_auth = State()

    teacher_menu = State()
    chose_student = State()
    chose_task = State()
    chose_submit = State()

    student_menu = State()
    task_menu_student = State()
    submit = State()



