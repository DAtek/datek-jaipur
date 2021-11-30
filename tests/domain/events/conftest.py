from pytest import fixture

from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.events.game_created import GameCreated

PLAYER1 = "Player1"
PLAYER2 = "Player2"


@fixture
async def initial_game() -> Game:
    event = GameCreated(player1_name=PLAYER1, player2_name=PLAYER2)
    await event.apply()

    return event.result
