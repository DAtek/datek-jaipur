from asyncio import run
from typing import AsyncGenerator

from datek_async_fsm.fsm import BaseFSM

from jaipur.adapters.console import ConsoleAdapter
from jaipur.state_machine.scope import Scope
from jaipur.state_machine.states import Start, Player1, Player2, End


class FSM(BaseFSM):
    scope: Scope

    async def _input_generator(self) -> AsyncGenerator[dict, None]:
        while True:
            yield {"scope": self.scope}


if __name__ == "__main__":
    scope = Scope(adapter_class=ConsoleAdapter)

    fsm = FSM([Start, Player1, Player2, End], scope=scope)
    run(fsm.run())
