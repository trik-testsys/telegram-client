import asyncio
import logging
import aiohttp

from repository.SubmitRepository import SubmitRepository
from teletrik.DI import service


@service
class GradingService:

    def __init__(self, submit_repository: SubmitRepository):
        self.url: str = "http://testsys:8080/grading-system/submissions/submission/"
        self.ERROR: str = "error"
        self.submit_repository: SubmitRepository = submit_repository

    async def update_all_submits_status(self):
        submits = await self.submit_repository.get_all_results()

        for submit in submits:

            if submit.result == "?":
                result = await self.get_submissions_status(submit.submit_id)
                print(f"Result {submit.submit_id}: {result}")
                submit.result = result if result != self.ERROR else submit.result
                submit.save()

    async def send_task(self, task_name: str, student_id: str, file) -> str:

        submit_id = await self._send_task(task_name, file)

        if submit_id != self.ERROR:
            await self.submit_repository.create_submit(submit_id, student_id, task_name)

        return submit_id

    async def get_submit(self, submit_id: str):
        return await self.get_submission(submit_id)

    async def get_submissions_status(self, submit_id: str) -> str:
        async with aiohttp.ClientSession() as session:

            async with session.get(f"{self.url}status", params={'id': submit_id}) as resp:

                match resp.status:

                    case 200:
                        return await resp.text()

                    case _:
                        return self.ERROR

    async def get_submission(self, submit_id: str):
        async with aiohttp.ClientSession() as session:

            async with session.get(f"{self.url}download", params={'id': submit_id}) as resp:

                match resp.status:

                    case 200:
                        return await resp.read()

                    case _:
                        return self.ERROR

    async def _send_task(self, task_name: str, file) -> str:
        params = {'task_name': task_name, 'file': file}
        timeout = aiohttp.ClientTimeout(total=5)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:

                async with session.post(f"{self.url}upload", data=params) as resp:
                    logging.info(f"STATUS = {resp.status}")
                    match resp.status:

                        case 200:
                            return await resp.text()

                        case _:
                            return self.ERROR

        except asyncio.exceptions.TimeoutError:
            logging.info("AAAAAAAAAAAAAAAAAAAAAAA")
            return self.ERROR
