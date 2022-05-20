from typing import List, Dict

from aiogram.types import Message

from bot.teletrik.DI import Handler, State


class MainHandler:

    def __init__(self, handlers: List[Handler]):
        self._handlers: List[Handler] = handlers
        self._states: Dict[int, str] = {}

    async def main_handler(self, message: Message):
        idr: int = message.from_user.id

        (command_handler, _, _) = self._find_command_handler()
        result: State = await command_handler(message)

        if result is None:
            (handler, _, _) = self._chose_handler(idr)
            new_state: str = await handler(message)
            self._states[idr] = new_state

            (_, prepare, _) = self._chose_handler(idr)
            await prepare(message)
        else:
            self._states[idr] = result
            (_, prepare, _) = self._chose_handler(idr)
            await prepare(message)

    def _chose_handler(self, idr: int) -> Handler:
        cur_state = self._states.get(idr)
        print(self._handlers)
        for (handler, prep, state) in self._handlers:
            if cur_state == state:
                return handler, prep, state
        raise Exception("TODO 4")

    def _find_command_handler(self) -> Handler:
        for (handler, prep, state) in self._handlers:
            if state == "command":
                return handler, prep, state
