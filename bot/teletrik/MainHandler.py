from typing import List, Dict

from aiogram.types import Message

from bot.teletrik.DI import Handler


class MainHandler:

    def __init__(self, handlers: List[Handler]):
        self._handlers: List[Handler] = sorted(handlers, key=lambda t: t[0])
        self._states: Dict[int, str] = {}

    async def main_handler(self, message: Message):
        idr: int = message.from_user.id

        (_, handler, _, _) = self._chose_handler(idr)
        new_state: str = await handler(message)
        self._states[idr] = new_state

        (_, _, prepare, _) = self._chose_handler(idr)
        await prepare(message)

    def _chose_handler(self, idr: int) -> Handler:
        cur_state = self._states.get(idr)
        for (order, handler, prep, state) in self._handlers:
            if cur_state == state:
                return order, handler, prep, state
        raise Exception("TODO 4")


