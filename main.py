import logging

from teletrik.Client import Client

if __name__ == "__main__":
    client: Client = Client(api_key="")
    client.run(log_level=logging.DEBUG)
