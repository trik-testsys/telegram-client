import logging


from bot.teletrik.Client import Client
from bot.utils import _read_key
import controller


if __name__ == "__main__":
    key: str = _read_key()
    client: Client = Client(key)
    client.run(log_level=logging.DEBUG)
