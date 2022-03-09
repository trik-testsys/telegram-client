from typing import Dict, List

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State
from aiogram.types import ContentType

_cls_instances: Dict[str, any] = {}
_obj_instances: Dict[str, any] = {}
_preparations: Dict[State, any] = {}


def Autowired(cls: type):
    if cls.__name__ not in _cls_instances.keys():
        _cls_instances[cls.__name__] = cls()

    return _cls_instances.get(cls.__name__)


def Singleton(obj: object):
    if obj.__class__.__name__ not in _obj_instances.keys():
        _obj_instances[obj.__class__.__name__] = obj

    return _obj_instances.get(obj.__class__.__name__)


async def ChangeState(state: State, message: types.Message):
    await state.set()
    await _preparations[state](message)


def StateController(state: State, dp: Dispatcher):
    print(state)
    def decorator(cls: type):

        hasHandler = "handler" in cls.__dict__
        hasPrepare = "prepare" in cls.__dict__

        if hasPrepare and hasHandler:
            dp.register_message_handler(cls.handler, state=state, content_types=ContentType.ANY)
            _preparations[state] = cls.prepare
        else:
            raise Exception("StateController must has prepare and handler method")

    return decorator


def CommandController(commands: List[str], dp: Dispatcher):
    print(commands)
    def decorator(cls: type):

        hasHandler = "handler" in cls.__dict__

        if hasHandler:
            dp.register_message_handler(cls.handler, commands=commands, state='*')

        else:
            raise Exception("CommandController must has handler method")

    return decorator


def Repository(cls: type):
    hasOnStart = "init_repository" in cls.__dict__

    if hasOnStart:
        cls.init_repository()

    else:
        raise Exception(f"Repository must has init_repository method")

    return cls
