import signal
from asyncio import create_task
from os import getpid
from subprocess import run
from threading import Thread
from time import sleep
from typing import Generator
from unittest.mock import Mock, patch

from datek_jaipur.application.adapters.console import adapter
from datek_jaipur.application.console import create_fsm, main
from pytest import fixture, mark
from tests.acceptance.application.utils import FakeStandardIO, Solver, timeout_watcher


@mark.asyncio
@patch.object(adapter, adapter.clear_screen.__name__, Mock())
@timeout_watcher(30)
async def test_game_played_multiple_times(patched_io, caplog):
    player1_name = "Player1"
    player2_name = "Player2"

    async def play_game():
        fsm = create_fsm()
        fsm_task = create_task(fsm.run())

        await patched_io.wait_for_output("enter player 1 name")
        # Enter invalid name
        patched_io.write_to_input("")

        await patched_io.wait_for_output("enter player 2 name")
        patched_io.write_to_input(player2_name)

        await patched_io.wait_for_output("invalid name")

        await patched_io.wait_for_output("enter player 1 name")
        patched_io.write_to_input(player1_name)
        await patched_io.wait_for_output("enter player 2 name")
        patched_io.write_to_input(player2_name)

        await patched_io.wait_for_output("Pick your action")
        # enter invalid command
        patched_io.write_to_input("asd")

        solver = Solver(player1_name, player2_name, patched_io)
        await solver.run()

        patched_io.write_to_input("asd")
        await patched_io.wait_for_output("Would you like to play again")
        patched_io.write_to_input("n")
        await fsm_task

        win_message = patched_io.output_collection[-3]
        assert "winner" in win_message

    for _ in range(5):
        await play_game()


def test_main_exits_on_sigint(patched_io):
    Thread(
        target=_send_signal_after_sleep, kwargs={"signal": signal.SIGINT}, daemon=True
    ).start()
    main()


def test_main_exits_on_sigterm(patched_io):
    Thread(
        target=_send_signal_after_sleep, kwargs={"signal": signal.SIGTERM}, daemon=True
    ).start()
    main()


def _send_signal_after_sleep(signal: int):
    sleep(0.1)
    run(f"kill -{signal} {getpid()}", shell=True)


@fixture
def patched_io() -> Generator[FakeStandardIO, None, None]:
    io = FakeStandardIO()

    with (
        patch.object(adapter, "input", io.input),
        patch.object(adapter, "print", io.print),
    ):
        yield io
