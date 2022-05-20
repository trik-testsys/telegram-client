import os
import sys

from bot.teletrik.DI import repository
from bot.model.User import User


@repository
class UserRepository:

    def __init__(self):
        User.create_table()

    async def get_all_users(self):
        return User.select()

    def get_all_students(self):
        result = [i.user_id for i in User.select().where(User.role == "student")]
        return result

    async def get_all_teachers(self):
        return User.select().where(User.role == "teacher")

    async def create_user(self, user_id: str, role: str) -> None:
        User.create(user_id=user_id, role=role)

    async def is_teacher(self, user_id):
        user = User.get(User.user_id == user_id)
        return user.role == "teacher"

    async def is_student(self, user_id):
        user = User.get(User.user_id == user_id)
        return user.role == "student"

    async def get_user(self, user_id):
        users = User.select().where(User.user_id == user_id)
        if len(users) == 0:
            return None
        else:
            return users[0]
