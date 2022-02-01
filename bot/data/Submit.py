import peewee as pw
from prettytable import PrettyTable

from bot.config import STUDENTS
from bot.loader import db, tasks


class Submit(pw.Model):
    submit_id = pw.CharField(unique=True, primary_key=True)
    student_id = pw.CharField()
    task_name = pw.CharField()
    result = pw.CharField()

    class Meta:
        database = db


async def create_submit(submit_id: str, student_id: str, task_name: str) -> None:
    Submit.create(submit_id=submit_id, student_id=student_id, task_name=task_name, result="?")


async def update_submit_result(submit_id: str, result: str) -> None:
    submit = Submit.get(Submit.submit_id == submit_id)
    submit.result = result
    submit.save()


async def get_all_results() -> list[Submit]:
    return Submit.select()


async def get_student_submits(student_id: str) -> list[Submit]:
    return Submit.select().where(Submit.student_id == student_id)


async def get_student_submits_by_task(student_id: str, task_name: str) -> list[Submit]:
    return Submit.select().where((Submit.student_id == student_id) & (Submit.task_name == task_name))


async def get_student_result(student_id: str) -> dict[str, str]:
    results = {}

    for task in tasks.keys():
        results[task] = "undef"

    for task in tasks.keys():
        student_result = await get_student_submits_by_task(student_id, task)
        status = ""
        cnt = str(len(student_result))

        for submit in student_result:

            match submit.result:
                case "+":
                    if status in ["", "-"]:
                        status = "+"

                case "-":
                    if status == "":
                        status = "-"

                case "?":
                    status = "?"

        results[task] = status + cnt

    return results


async def get_student_submits_view(student_id: str, task_name: str) -> PrettyTable:
    results = await get_student_submits_by_task(student_id, task_name)
    table = PrettyTable()

    table.field_names = ["Id послыки",  "Результат"]
    for result in results:
        table.add_row([result.submit_id,  result.result])

    return table


def init_database():
    Submit.create_table()


async def get_all_results_view():
    table = PrettyTable()
    title = ['Ученик']

    for task_name in tasks.keys():
        title.append(task_name)

    table.field_names = title

    for student in STUDENTS:
        student_result = await get_student_result(student)

        results = [student]
        for result in student_result.keys():
            results.append(student_result[result])
        table.add_row(results)

    return table


async def test_database():
    await create_submit("100", "10", "sample_task_1")
    await create_submit("101", "10", "sample_task_2")
    await update_submit_result("101", "+")
    await create_submit("102", "11", "sample_task_1")
    await update_submit_result("102", "-")
    await create_submit("103", "11", "sample_task_1")
    result = await get_student_submits("10")
    for i in result:
        print(i)
