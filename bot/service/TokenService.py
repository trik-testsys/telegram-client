from bot.teletrik.DI import service
from time import time
from hashlib import md5


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
