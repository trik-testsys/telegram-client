from abc import ABCMeta, abstractmethod

from aiogram.types import Message


class Controller(metaclass=ABCMeta):

    @abstractmethod
    async def handle(self, message: Message) -> str:
        pass

    @abstractmethod
    async def prepare(self, message: Message):
        pass
