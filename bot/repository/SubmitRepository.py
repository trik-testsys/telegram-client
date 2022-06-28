from bot.model.Submit import Submit
from bot.repository.TaskRepository import TaskRepository
from bot.teletrik.DI import repository


@repository
class SubmitRepository:
    def __init__(self, task_repository: TaskRepository):
        Submit.create_table()
        self.task_repository: TaskRepository = task_repository

    @staticmethod
    async def create_submit(submit_id: str, student_id: str, task_name: str) -> None:
        Submit.create(
            submit_id=submit_id, student_id=student_id, task_name=task_name, result="?"
        )

    @staticmethod
    async def get_submit(submit_id: str) -> Submit:
        return Submit.get(Submit.submit_id == submit_id)

    @staticmethod
    async def get_submit_or_none(submit_id: str) -> Submit | None:
        return Submit.get_or_none(Submit.submit_id == submit_id)

    @staticmethod
    async def update_submit_result(submit_id: str, result: str) -> None:
        submit: Submit = Submit.get(Submit.submit_id == submit_id)
        submit.result = result
        submit.save()

    @staticmethod
    async def get_all_results() -> list[Submit]:
        return Submit.select()

    @staticmethod
    async def get_student_submits(student_id: str) -> list[Submit]:
        return Submit.select().where(Submit.student_id == student_id)

    @staticmethod
    async def get_student_submits_by_task(
            student_id: str, task_name: str
    ) -> list[Submit]:
        return Submit.select().where(
            (Submit.student_id == student_id) & (Submit.task_name == task_name)
        )
