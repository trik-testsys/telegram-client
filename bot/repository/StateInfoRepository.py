from utils.injector import Repository


class StateInfo:
    chosen_task = ""
    chosen_student = ""

    def __init__(self, user_id):
        self.user_id = user_id


@Repository
class StateInfoRepository:

    state_info: dict[str, StateInfo] = {}

    @classmethod
    def init_repository(cls):
        pass

    @classmethod
    def create(cls, telegram_id: str, user_id: str):
        cls.state_info[telegram_id] = StateInfo(user_id)

    @classmethod
    def get(cls, telegram_id) -> StateInfo:
        return cls.state_info[telegram_id]
