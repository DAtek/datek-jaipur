from asyncio import Task, sleep, create_task, gather, CancelledError
from functools import wraps
from queue import Queue, Empty
from random import choice
from typing import Callable

from datek_jaipur.application.adapters.console.adapter import ConsoleGoodsType
from datek_jaipur.utils import run_in_thread_pool


class FakeStandardIO:
    def __init__(self, timeout=0.5):
        self.output_collection = []
        self._input_queue = Queue()
        self._output_queue = Queue()
        self._timeout = timeout

    def print(self, message: str = "", **kwargs):
        print(message)
        self.output_collection.append(message)
        self._output_queue.put(message)

    def input(self, prompt: str = "") -> str:
        print(prompt, end="")
        self.output_collection.append(prompt)
        self._output_queue.put(prompt)
        return self._input_queue.get()

    def write_to_input(self, message: str):
        print(message)
        self.output_collection.append(message)
        self._input_queue.put(message)

    async def wait_for_output(self, message: str, timeout: float = None) -> str:
        timeout = timeout if timeout is not None else self._timeout
        return await run_in_thread_pool(self._wait_for, message, timeout=timeout)

    def _wait_for(self, message: str, timeout: float) -> str:
        while True:
            item = self._output_queue.get(timeout=timeout)
            if message.lower() in item.lower():
                return item


class Solver:
    def __init__(self, player1_name: str, player2_name: str, io: FakeStandardIO):
        self._player1 = player1_name
        self._player2 = player2_name
        self._io = io
        self._turn_info = ""

    async def run(self):
        self._turn_info = await self._io.wait_for_output(_TURN_INFO_CONTENT_PART)

        while True:
            try:
                await self._simulate_turn()
            except Empty:
                return

    async def _simulate_turn(self):
        method = (
            self._simulate_player1
            if self._player1 in self._turn_info
            else self._simulate_player2
        )
        await method()

    async def _simulate_player1(self):
        while self._player1 in self._turn_info:
            await self._try_to_buy(self._player1)
            await self._try_to_sell(self._player1)

    async def _simulate_player2(self):
        while self._player2 in self._turn_info:
            await self._simulate_trading_nonexistent_card()
            await self._simulate_trading_different_amount_of_cards()

            if choice([True, False, False, False]):
                await self._try_to_trade(self._player2)

            await self._try_to_sell(self._player2)
            await self._simulate_buying_nonexistent_card()
            await self._try_to_buy(self._player2)

    async def _try_to_buy(self, player_name: str):
        for item in ConsoleGoodsType:
            if player_name not in self._turn_info:
                return

            self._io.write_to_input("b")
            await self._io.wait_for_output("buy")
            await self._pick_a_card(item.name)

    async def _try_to_sell(self, player_name: str):
        for item in ConsoleGoodsType:
            if player_name not in self._turn_info:
                return

            self._io.write_to_input("s")
            await self._io.wait_for_output("sell")
            await self._pick_a_card(item.name)

    async def _try_to_trade(self, player_name: str):
        for source in ConsoleGoodsType:
            for target in ConsoleGoodsType:
                if player_name not in self._turn_info:
                    return

                self._io.write_to_input("t")
                await self._io.wait_for_output("have")
                self._io.write_to_input(target.name)
                await self._io.wait_for_output("throw away")
                await self._pick_a_card(source.name)

    async def _simulate_buying_nonexistent_card(self):
        self._io.write_to_input("b")
        await self._io.wait_for_output("buy")
        await self._pick_a_card("")

    async def _simulate_trading_nonexistent_card(self):
        self._io.write_to_input("t")
        await self._io.wait_for_output("have")
        self._io.write_to_input("")
        await self._io.wait_for_output("throw away")
        await self._pick_a_card("")

    async def _simulate_trading_different_amount_of_cards(self):
        self._io.write_to_input("t")
        await self._io.wait_for_output("have")
        self._io.write_to_input("g d")
        await self._io.wait_for_output("throw away")
        await self._pick_a_card("c")

    async def _pick_a_card(self, card: str):
        self._io.write_to_input(card)
        self._turn_info = await self._io.wait_for_output(_TURN_INFO_CONTENT_PART)


def timeout_watcher(timeout_sec=1.0):
    func_: Callable = ...
    timeout_sec_: float = ...

    async def wrapper(*args, **kwargs):
        nonlocal func_
        nonlocal timeout_sec_

        func_task: Task = ...
        timeout_task: Task = ...

        async def timeout_watcher_():
            nonlocal func_task
            try:
                await sleep(timeout_sec_)
            except CancelledError:
                return
            func_task.cancel()
            raise TimeoutError

        async def run_func():
            nonlocal timeout_task
            result = await func_(*args, **kwargs)
            timeout_task.cancel()
            return result

        func_task = create_task(run_func())
        timeout_task = create_task(timeout_watcher_())

        results = await gather(func_task, timeout_task)

        return results[0]

    if callable(timeout_sec):
        func_ = timeout_sec
        timeout_sec_ = 1.0
        return wraps(func_)(wrapper)
    else:
        timeout_sec_ = timeout_sec

        def decorator(func):
            nonlocal func_
            func_ = func
            return wraps(func)(wrapper)

        return decorator


_TURN_INFO_CONTENT_PART = "it's your turn"
