from abc import abstractmethod
from asyncio import Future, get_event_loop
from functools import partial
from threading import Thread
from typing import Any, Callable, Generic, TypeVar

from datek_jaipur.errors import EventAlreadyAppliedError, EventNotAppliedError

Result = TypeVar("Result")


class BaseEvent(Generic[Result]):
    __slots__ = ["_result", "_data_model"]

    def __init__(self, **kwargs):
        self._result = ...
        data_model_type = self.__class__.__annotations__.get("_data_model")
        self._data_model = data_model_type(**kwargs) if data_model_type else None

    @property
    def result(self) -> Result:
        if self._result is ...:
            raise EventNotAppliedError

        return self._result

    async def apply(self):
        if self._result is not ...:
            raise EventAlreadyAppliedError

        await self._validate()
        self._result = await self._create_result()

    async def _validate(self):
        pass

    @abstractmethod
    async def _create_result(self) -> Result:  # pragma: no cover
        pass


async def run_in_thread_pool(func, *args, **kwargs):
    executor = CustomThreadExecutor(func, *args, **kwargs)
    return await executor.run()


class CustomThreadExecutor:
    def __init__(self, func: Callable, *args, **kwargs):
        self._loop = get_event_loop()
        self._result: Future = Future()
        self._func = func
        self._args = args
        self._kwargs = kwargs

    async def run(self) -> Any:
        thread = Thread(target=self._run, daemon=True)
        thread.start()
        await self._result
        result = self._result.result()
        if isinstance(result, Exception):
            raise result

        return result

    def _run(self):
        try:
            result = self._func(*self._args, **self._kwargs)
        except Exception as error:
            result = error

        set_result = partial(self._result.set_result, result)
        self._loop.call_soon_threadsafe(set_result)
