from model.User import User
from utils.injector import Repository


@Repository
class UserRepository:

    @classmethod
    def init_repository(cls):
        User.create_table()

    @classmethod
    async def get_all_users(cls):
        return User.select()

    @classmethod
    def get_all_students(cls):
        result = [i.user_id for i in User.select().where(User.role == "student")]
        return result

    @classmethod
    async def get_all_teachers(cls):
        return User.select().where(User.role == "teacher")

    @classmethod
    async def create_user(cls, user_id: str, role: str) -> None:
        User.create(user_id=user_id, role=role)

    @classmethod
    async def is_teacher(cls, user_id):
        user = User.get(User.user_id == user_id)
        return user.role == "teacher"

    @classmethod
    async def is_student(cls, user_id):
        user = User.get(User.user_id == user_id)
        return user.role == "student"



