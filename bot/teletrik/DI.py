from typing import List, Dict, Type, Set, Callable, Tuple, TypeAlias, Coroutine, Any
from aiogram.types import Message

from bot.teletrik.Controller import Controller

st = str

HandlerFunc: TypeAlias = Callable[[Message], Coroutine[Any, Any, st]]
Handler: TypeAlias = Tuple[int, HandlerFunc, HandlerFunc, st]

_classes: Set[Type] = set()
_instances: Dict[Type, object] = {}
_handlers: List[Handler] = []
_controllers: List[Tuple[Type[Controller], st, int]] = []


def _init_cls(cls) -> object:
    obj: object = _instances.get(cls)
    if obj is not None:
        return obj

    init_args = cls.__init__.__annotations__
    args: List[object] = []
    for arg_name in init_args:
        arg_type = init_args[arg_name]
        args.append(_init_cls(arg_type))

    obj = cls(*args)
    _instances[cls] = obj

    return obj


def _init_controller(cls: Type[Controller]) -> Controller:
    init_args = cls.__init__.__annotations__
    args: List[object] = []
    for arg_name in init_args:
        arg_type = init_args[arg_name]
        args.append(_init_cls(arg_type))

    return cls(*args)


def controller(state: str = None, order: int = 10):

    def f(cls):
        if issubclass(cls, Controller) and cls not in _classes:
            _controllers.append((cls, state, order))
        return cls

    return f


def repository(cls: Type) -> Type:
    return inject(cls)


def service(cls: Type) -> Type:
    return inject(cls)


def inject(cls: Type) -> Type:
    if cls not in _classes:
        _classes.add(cls)
    return cls


def get_handlers() -> List[Handler]:
    result: List[Handler] = []
    for (cont, state, order) in _controllers:
        obj: Controller = _init_controller(cont)
        handler: HandlerFunc = obj.handle
        prepare: HandlerFunc = obj.prepare
        result.append((order, handler, prepare, state))
    return result
