from typing import Dict, List

from aiogram.types import Message
from bot.teletrik.DI import Handler, State


class MainHandler:
    def __init__(self, handlers: List[Handler]):
        self._handlers: List[Handler] = handlers
        self._states: Dict[int, str] = {}

    async def main_handler(self, message: Message):
        idr: int = message.from_user.id
        cur_state: State = self._states.get(idr)

        if cur_state is None:
            cur_state = "command"

        (command_handler, _, _) = self._find_command_handler()
        result: State | None = await command_handler(message)

        if result is not None:
            self._states[idr] = result
            (_, prepare, _) = self._chose_handler(idr)
            await prepare(message)

        else:
            (handler, _, _) = self._chose_handler(idr)
            new_state: str = await handler(message)
            self._states[idr] = new_state

            if cur_state != new_state:
                (_, prepare, _) = self._chose_handler(idr)
                await prepare(message)

    def _chose_handler(self, idr: int) -> Handler:
        cur_state = self._states.get(idr)
        print(self._states)
        for (handler, prep, state) in self._handlers:
            if cur_state == state:
                return handler, prep, state
        raise Exception("TODO 4")

    def _find_command_handler(self) -> Handler:
        for (handler, prep, state) in self._handlers:
            if state == "command":
                return handler, prep, state
