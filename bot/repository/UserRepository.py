from typing import List

from bot.model.User import User
from bot.teletrik.DI import repository


@repository
class UserRepository:
    def __init__(self) -> None:
        User.create_table()

    @staticmethod
    async def get_by_role(role: str) -> List[User]:
        return User.select().where(User.role == role)

    @staticmethod
    async def create_user(user_id: str, role: str, tg_id: str) -> None:
        User.create(user_id=user_id, role=role, telegram_id=tg_id)

    @staticmethod
    async def get_by_user_id(user_id: str) -> User | None:
        return User.get_or_none(User.user_id == user_id)

    @staticmethod
    async def get_by_telegram_id(telegram_id: str) -> User | None:
        return User.get_or_none(User.telegram_id == telegram_id)
