import logging

from bot.conf import PATH_TO_KEY
from bot.teletrik.Client import Client
import controller


def _read_key() -> str:
    key_file = open(PATH_TO_KEY, "r")
    api_key = key_file.read()
    key_file.close()
    return api_key


if __name__ == "__main__":
    key: str = _read_key()
    client: Client = Client(key)
    client.run(log_level=logging.DEBUG)
