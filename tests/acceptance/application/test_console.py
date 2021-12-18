from asyncio import create_task
from unittest.mock import patch, Mock

from pytest import mark, fixture

from datek_jaipur.application.adapters.console import adapter
from datek_jaipur.application.console import create_fsm
from tests.acceptance.application.utils import FakeStandardIO, Solver, timeout_watcher


@mark.asyncio
@patch.object(adapter, adapter.clear_screen.__name__, Mock())
@timeout_watcher(5)
async def test_game_played(patched_io, caplog):
    player1_name = "Player1"
    player2_name = "Player2"

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


@fixture
def patched_io() -> FakeStandardIO:
    io = FakeStandardIO()

    with (
        patch.object(adapter, "input", io.input),
        patch.object(adapter, "print", io.print),
    ):
        yield io
