import asyncio

from bot.data.Submit import get_all_results, create_submit
from bot.grading import GradingServer


async def update_all_submits_status():
    submits = await get_all_results()

    for submit in submits:

        if submit.result == "?":
            submit.result = await GradingServer.get_submissions_status(submit.submit_id)
            submit.save()


async def start_polling():
    await update_all_submits_status()
    await asyncio.sleep(30)
    await start_polling()


async def send_task(task_name: str, student_id: str, file) -> str:
    submit_id = await GradingServer.send_task(task_name, file)
    await create_submit(submit_id, student_id, task_name)
    return submit_id


async def get_submit(submit_id: str):
    return await GradingServer.get_submission(submit_id)
