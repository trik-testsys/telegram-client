from bot.conf import PATH_TO_KEY


def _read_key() -> str:
    key_file = open(PATH_TO_KEY, "r")
    api_key = key_file.read().strip()
    key_file.close()
    return api_key
