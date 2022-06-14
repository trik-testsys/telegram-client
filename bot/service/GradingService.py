import asyncio
import logging

import aiohttp
from bot.conf import GRADING_SERVICE_URL
from bot.repository.SubmitRepository import SubmitRepository
from bot.teletrik.DI import service


@service
class GradingService:
    def __init__(self, submit_repository: SubmitRepository):
        self.url: str = f"{GRADING_SERVICE_URL}grading-system/submissions/submission/"
        self.SERVER_ERROR: str = "error"
        self.USER_ERROR: str = "user_error"
        self.submit_repository: SubmitRepository = submit_repository

    async def scheduled(self):
        await self.update_all_submits_status()

    async def update_all_submits_status(self):
        submits = await self.submit_repository.get_all_results()

        for submit in submits:

            if submit.result == "?":
                result = await self.get_submissions_status(submit.submit_id)
                print(f"Result {submit.submit_id}: {result}")
                submit.result = result if result != self.SERVER_ERROR else submit.result
                submit.save()

    async def send_task(self, task_name: str, student_id: str, file) -> str:

        submit_id = await self._send_task(task_name, file)

        if submit_id != self.SERVER_ERROR:
            await self.submit_repository.create_submit(submit_id, student_id, task_name)

        return submit_id

    async def get_submissions_status(self, submit_id: str) -> str:
        return await self._get_request(f"{self.url}status", params={"id": submit_id})

    async def get_submission(self, submit_id: str):
        return await self._get_request(f"{self.url}download", params={"id": submit_id})

    async def get_lektorium_info(self, submit_id: str):
        return await self._get_request(
            f"{self.url}lectorium_info", params={"id": submit_id}
        )

    async def _send_task(self, task_name: str, file) -> str:
        params = {"task_name": task_name, "file": file}
        timeout = aiohttp.ClientTimeout(total=5)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:

                async with session.post(f"{self.url}upload", data=params) as resp:
                    logging.info(f"STATUS = {resp.status}")
                    match resp.status:

                        case 200:
                            return await resp.text()

                        case 422:
                            return self.USER_ERROR

                        case _:
                            return self.SERVER_ERROR

        except asyncio.exceptions.TimeoutError:
            return self.SERVER_ERROR
        except aiohttp.client_exceptions.ClientConnectionError:
            return self.SERVER_ERROR

    async def _get_request(self, url: str, params: dict[str, str]) -> str:
        timeout = aiohttp.ClientTimeout(total=5)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:

                async with session.get(url, params=params) as resp:
                    match resp.status:

                        case 200:
                            return await resp.text()

                        case _:
                            return self.SERVER_ERROR

        except asyncio.exceptions.TimeoutError:
            return self.SERVER_ERROR
        except aiohttp.client_exceptions.ClientConnectionError:
            return self.SERVER_ERROR
