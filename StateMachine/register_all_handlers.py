from aiogram import Dispatcher
from aiogram.types import ContentType

from bot.StateMachine.StateMachine import StateMachine
from bot.StateMachine.auth_states import WaitAuthState
from bot.StateMachine.student_states import TaskMenuState, StudentMenuState, SubmitState
from bot.StateMachine.teacher_states import TeacherMenuState, ChoseStudentState, ChoseTaskState, ChoseSubmitState


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(WaitAuthState.handler, state=StateMachine.wait_auth)
    dp.register_message_handler(TeacherMenuState.handler, state=StateMachine.teacher_menu)
    dp.register_message_handler(StudentMenuState.handler, state=StateMachine.student_menu)
    dp.register_message_handler(TaskMenuState.handler, state=StateMachine.task_menu_student)
    dp.register_message_handler(SubmitState.handler, state=StateMachine.submit,
                                content_types=ContentType.ANY)
    dp.register_message_handler(ChoseStudentState.handler, state=StateMachine.chose_student)
    dp.register_message_handler(ChoseTaskState.handler, state=StateMachine.chose_task)
    dp.register_message_handler(ChoseSubmitState.handler, state=StateMachine.chose_submit)


