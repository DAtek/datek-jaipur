from pytest import fixture

from jaipur.compound_types.game import Game
from jaipur.events.game_created import GameCreated


PLAYER1 = "Player1"
PLAYER2 = "Player2"


@fixture
def initial_game() -> Game:
    event = GameCreated(PLAYER1, PLAYER2)
    event.apply()

    return event.result
