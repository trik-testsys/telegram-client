from time import sleep

import aiohttp

url = "url to grading server"
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
    async with aiohttp.ClientSession() as session:

        async with session.post(f"{url}upload", data=params) as resp:
            print(resp.status)
            print(await resp.text())

            match resp.status:

                case 200:
                    return await resp.text()

                case _:
                    return ERROR


async def test_grading():
    # kek = await send_task("task1", "2.1.3 (3).qrs")
    # sleep(60)
    print(await get_submissions_status("1000000"))
