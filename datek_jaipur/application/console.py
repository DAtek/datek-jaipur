from asyncio import run
import signal

from datek_jaipur.application.adapters.console.adapter import ConsoleAdapter
from datek_jaipur.application.state_machine.fsm import FSM
from datek_jaipur.application.state_machine.scope import Scope
from datek_jaipur.application.state_machine.states import (
    Start,
    PlayerTurn,
    End,
    PlayerWon,
)


class ExitError(Exception):
    pass


def main():
    fsm = create_fsm()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    try:
        run(fsm.run())
    except ExitError:
        pass


def create_fsm() -> FSM:
    scope = Scope(adapter_class=ConsoleAdapter)
    return FSM([Start, PlayerTurn, PlayerWon, End], scope=scope)


def _stop(signum, frame):
    raise ExitError
