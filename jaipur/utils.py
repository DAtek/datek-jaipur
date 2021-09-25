from abc import abstractmethod
from functools import wraps
from typing import TypeVar, Generic

from jaipur.errors import EventAlreadyAppliedError, EventNotAppliedError
from jaipur.log import create_logger

logger = create_logger(__name__)


class EventMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        class_ = super().__new__(mcs, name, bases, namespace)

        def log_event(func: callable):
            @wraps(func)
            def wrapper(self):
                result = func(self)
                logger.debug(f"{self} Result: {self.result}")
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