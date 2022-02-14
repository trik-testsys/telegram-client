from time import sleep

import aiohttp

url = "http://192.168.1.243:8080/grading-system/submissions/submission/"
ERROR = "error"


async def get_submissions_status(submit_id: str) -> str:
    async with aiohttp.ClientSession() as session:

        async with session.get(f"{url}status", params={'id': submit_id}) as resp:

            match resp.status:

                case 200:
                    return await resp.text()

                case _:
                    return ERROR


async def get_submission(submit_id: str):
    async with aiohttp.ClientSession() as session:

        async with session.get(f"{url}download", params={'id': submit_id}) as resp:
            print(resp.status)
            match resp.status:

                case 200:
                    return await resp.read()

                case _:
                    return ERROR


async def send_task(task_name: str, file) -> str:
    params = {'task_name': task_name, 'file': file}
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:

        async with session.post(f"{url}upload", data=params) as resp:

            match resp.status:

                case 200:
                    return await resp.text()

                case _:
                    return ERROR


