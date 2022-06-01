from bot.teletrik.DI import repository


class StateInfo:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.chosen_task = ""
        self.chosen_student = ""


@repository
class StateInfoRepository:
    def __init__(self) -> None:
        self.state_info: dict[str, StateInfo] = {}

    def create(self, telegram_id: str, user_id: str) -> None:
        self.state_info[telegram_id] = StateInfo(user_id)

    def get(self, telegram_id) -> StateInfo:
        return self.state_info[telegram_id]
