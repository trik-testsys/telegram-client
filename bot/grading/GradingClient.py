import asyncio

from bot.data.Submit import get_all_results, create_submit
from bot.grading import GradingServer
from bot.grading.GradingServer import ERROR


async def update_all_submits_status():
    submits = await get_all_results()

    for submit in submits:

        if submit.result == "?":
            result = await GradingServer.get_submissions_status(submit.submit_id)
            submit.result = result if result != ERROR else submit.result
            submit.save()


async def send_task(task_name: str, student_id: str, file) -> str:
    print("kek")
    submit_id = await GradingServer.send_task(task_name, file)

    if submit_id != ERROR:
        await create_submit(submit_id, student_id, task_name)

    return submit_id


async def get_submit(submit_id: str):
    return await GradingServer.get_submission(submit_id)
