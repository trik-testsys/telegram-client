from aiogram import Bot
from bot.conf import PATH_TO_ADMINS, PATH_TO_KEY


def _read_key() -> str:
    key_file = open(PATH_TO_KEY, "r")
    api_key = key_file.read().strip()
    key_file.close()
    return api_key


def _read_admins() -> list[int]:
    admins_file = open(PATH_TO_ADMINS, "r")
    admins = list(map(lambda x: int(x.strip()), admins_file.read().split()))
    admins_file.close()
    return admins


async def alert_admins(bot: Bot):
    for admin_id in _read_admins():
        await bot.send_message(admin_id, "Бот перезапущен")
