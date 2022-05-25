import logging

from bot.teletrik.Client import Client
import controller

if __name__ == "__main__":
    client: Client = Client(api_key="")
    client.run(log_level=logging.DEBUG)
