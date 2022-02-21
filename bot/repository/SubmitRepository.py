from prettytable import PrettyTable

from bot.repository.TaskRepository import TaskRepository
from bot.repository.UserRepository import UserRepository
from model.Submit import Submit
from utils.injector import Repository


@Repository
class SubmitRepository:

    taskRepository = TaskRepository
    userRepository = UserRepository

    @classmethod
    def init_repository(cls):
        Submit.create_table()

    @classmethod
    async def create_submit(cls, submit_id: str, student_id: str, task_name: str) -> None:
        Submit.create(submit_id=submit_id, student_id=student_id, task_name=task_name, result="?")

    @classmethod
    async def update_submit_result(cls, submit_id: str, result: str) -> None:
        submit = Submit.get(Submit.submit_id == submit_id)
        submit.result = result
        submit.save()

    @classmethod
    async def get_all_results(cls) -> list[Submit]:
        return Submit.select()

    @classmethod
    async def get_student_submits(cls, student_id: str) -> list[Submit]:
        return Submit.select().where(Submit.student_id == student_id)

    @classmethod
    async def get_student_submits_by_task(cls, student_id: str, task_name: str) -> list[Submit]:
        return Submit.select().where((Submit.student_id == student_id) & (Submit.task_name == task_name))

    @classmethod
    async def get_student_result(cls, student_id: str) -> dict[str, str]:
        results = {}

        for task in TaskRepository.get_tasks():
            results[task] = "undef"

        for task in TaskRepository.get_tasks():
            student_result = await cls.get_student_submits_by_task(student_id, task)
            status = ""
            cnt = str(len(student_result))

            for submit in student_result:

                match submit.result:
                    case "+":
                        if status in ["", "-", "?"]:
                            status = "+"

                    case "-":
                        if status == "":
                            status = "-"

                    case "?":
                        if status in ["", "-"]:
                            status = "?"

            results[task] = status + cnt

        return results

    @classmethod
    async def get_student_submits_view(cls, student_id: str, task_name: str) -> PrettyTable:
        results = await cls.get_student_submits_by_task(student_id, task_name)
        table = PrettyTable()

        table.field_names = ["Id послыки", "Результат"]
        for result in results:
            table.add_row([result.submit_id, result.result])

        return table

    @classmethod
    async def get_all_results_view(cls):
        table = PrettyTable()
        title = ['Ученик']

        for task_name in cls.taskRepository.get_tasks().keys():
            title.append(task_name)

        table.field_names = title

        for student in cls.userRepository.get_all_students():
            student_result = await cls.get_student_result(student)

            results = [student]
            for result in student_result.keys():
                results.append(student_result[result])
            table.add_row(results)

        return table
