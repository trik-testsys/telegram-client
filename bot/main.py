import logging

from bot.teletrik.Client import Client
import controller

if __name__ == "__main__":
    client: Client = Client(api_key="5022193517:AAGFF1LLBGuly1V_1eApKM_3H1S4hkoX9lw")
    client.run(log_level=logging.DEBUG)
