from typing import Any, Callable, Coroutine, Dict, List, Set, Tuple, Type, TypeAlias

from aiogram.types import Message
from bot.teletrik.Controller import Controller

State: TypeAlias = str | None
Command: State = "command"

HandlerFunc: TypeAlias = Callable[[Message], Coroutine[Any, Any, State]]
Handler: TypeAlias = Tuple[HandlerFunc, HandlerFunc, State]

_classes: Set[Type] = set()
_instances: Dict[Type, object] = {}
_handlers: List[Handler] = []
_controllers: List[Tuple[Type[Controller], State]] = []


def _init_cls(cls) -> object:
    obj: object = _instances.get(cls)
    if obj is not None:
        return obj

    init_args = cls.__init__.__annotations__
    args: List[object] = []
    for arg_name in init_args:
        arg_type = init_args[arg_name]
        if arg_type is not None:
            args.append(_init_cls(arg_type))

    obj = cls(*args)
    _instances[cls] = obj

    return obj


def _init_controller(cls: Type[Controller]) -> Controller:
    init_args = cls.__init__.__annotations__
    args: List[object] = []
    print(init_args)
    for arg_name in init_args:
        arg_type = init_args[arg_name]
        if arg_type is not None:
            args.append(_init_cls(arg_type))

    return cls(*args)


def controller(state: str = None):
    def f(cls):
        if issubclass(cls, Controller) and cls not in _classes:
            _controllers.append((cls, state))
        else:
            raise Exception("TODO 5")
        return cls

    return f


def repository(cls: Type) -> Type:
    return inject(cls)


def service(cls: Type) -> Type:
    return inject(cls)


def view(cls: Type) -> Type:
    return inject(cls)


def inject(cls: Type) -> Type:
    if cls not in _classes:
        _classes.add(cls)
    return cls


def get_jobs():
    res = []
    for obj in _instances.values():
        if obj.__class__.__dict__.get("scheduled") is not None:
            res.append(obj.scheduled)
    return res


def get_handlers() -> List[Handler]:
    result: List[Handler] = []
    for (cont, state) in _controllers:
        obj: Controller = _init_controller(cont)
        handler: HandlerFunc = obj.handle
        prepare: HandlerFunc = obj.prepare
        result.append((handler, prepare, state))
    return result
