from abc import ABCMeta, abstractmethod
from asyncio import get_event_loop
from functools import wraps, partial
from typing import TypeVar, Generic, Callable

from jaipur.errors import EventAlreadyAppliedError, EventNotAppliedError
from jaipur.log import create_logger

logger = create_logger(__name__)


class EventMeta(ABCMeta):
    def __new__(cls, name: str, bases: tuple, namespace: dict):
        class_ = super().__new__(cls, name, bases, namespace)

        def log_event(func: Callable):
            @wraps(func)
            def wrapper(self):
                result = func(self)
                logger.debug("%s Result: %s", result, self.result)
                return result

            return wrapper

        class_.apply = log_event(class_.apply)

        return class_


Result = TypeVar("Result")


class BaseEvent(Generic[Result], metaclass=EventMeta):
    _result: Result

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._result = ...
        return obj

    def apply(self):
        if self._result is not ...:
            raise EventAlreadyAppliedError

        self.validate()
        self._result = self._create_result()

    @property
    def result(self) -> Result:
        if self._result is ...:
            raise EventNotAppliedError

        return self._result

    def validate(self):
        pass

    @abstractmethod
    def _create_result(self) -> Result:  # pragma: no cover
        pass


async def run_in_thread_pool(func, *args, **kwargs):
    loop = get_event_loop()
    partial_ = partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, partial_)
