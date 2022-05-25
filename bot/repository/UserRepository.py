from typing import List

from bot.teletrik.DI import repository
from bot.model.User import User


@repository
class UserRepository:

    def __init__(self):
        User.create_table()

    @staticmethod
    async def get_all_users():
        return User.select()

    @staticmethod
    def get_all_students():
        result = [i.user_id for i in User.select().where(User.role == "student")]
        return result

    @staticmethod
    async def create_user(user_id: str, role: str, tg_id: str) -> None:
        User.create(user_id=user_id, role=role, telegram_id=tg_id)

    @staticmethod
    async def get_by_user_id(user_id: str) -> User | None:
        return User.get_or_none(User.user_id == user_id)

    @staticmethod
    async def get_by_telegram_id(telegram_id: str) -> User | None:
        return User.get_or_none(User.telegram_id == telegram_id)

    @staticmethod
    async def user_exist(user_id: str) -> bool:
        users: List[User] = User().select().where(User.user_id == user_id)
        return len(users) == 0

