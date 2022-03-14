import asyncio
import logging
import aiohttp

from bot.repository.SubmitRepository import SubmitRepository


class GradingService:
    url = "http://testsys:8080/grading-system/submissions/submission/"
    ERROR = "error"

    @classmethod
    async def update_all_submits_status(cls):
        submits = await SubmitRepository.get_all_results()

        for submit in submits:

            if submit.result == "?":
                result = await cls.get_submissions_status(submit.submit_id)
                print(f"Result {submit.submit_id}: {result}")
                submit.result = result if result != cls.ERROR else submit.result
                submit.save()

    @classmethod
    async def send_task(cls, task_name: str, student_id: str, file) -> str:

        submit_id = await cls._send_task(task_name, file)

        if submit_id != cls.ERROR:
            await SubmitRepository.create_submit(submit_id, student_id, task_name)

        return submit_id

    @classmethod
    async def get_submit(cls, submit_id: str):
        return await cls.get_submission(submit_id)

    @classmethod
    async def get_submissions_status(cls, submit_id: str) -> str:
        async with aiohttp.ClientSession() as session:

            async with session.get(f"{cls.url}status", params={'id': submit_id}) as resp:

                match resp.status:

                    case 200:
                        return await resp.text()

                    case _:
                        return cls.ERROR

    @classmethod
    async def get_submission(cls, submit_id: str):
        async with aiohttp.ClientSession() as session:

            async with session.get(f"{cls.url}download", params={'id': submit_id}) as resp:

                match resp.status:

                    case 200:
                        return await resp.read()

                    case _:
                        return cls.ERROR

    @classmethod
    async def _send_task(cls, task_name: str, file) -> str:
        params = {'task_name': task_name, 'file': file}
        timeout = aiohttp.ClientTimeout(total=5)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:

                async with session.post(f"{cls.url}upload", data=params) as resp:
                    logging.info(f"STATUS = {resp.status}")
                    match resp.status:

                        case 200:
                            return await resp.text()

                        case _:
                            return cls.ERROR

        except asyncio.exceptions.TimeoutError:
            logging.info("AAAAAAAAAAAAAAAAAAAAAAA")
            return cls.ERROR
