from bot.teletrik.DI import repository


class StateInfo:
    chosen_task = ""
    chosen_student = ""

    def __init__(self, user_id):
        self.user_id = user_id


@repository
class StateInfoRepository:
    def __init__(self):
        self.state_info: dict[str, StateInfo] = {}

    def create(self, telegram_id: str, user_id: str):
        self.state_info[telegram_id] = StateInfo(user_id)

    def get(self, telegram_id) -> StateInfo:
        return self.state_info[telegram_id]
