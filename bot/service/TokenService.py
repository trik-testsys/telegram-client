from hashlib import md5
from time import time

from bot.teletrik.DI import service


@service
class TokenService:
    def __init__(self):
        pass

    @staticmethod
    def generate_new_token(tg_id: str) -> str:
        cur_time: float = time()
        md5_hash = md5((str(cur_time) + str(tg_id)).encode())
        token: str = md5_hash.hexdigest()
        return token
