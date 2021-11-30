from dataclasses import dataclass
from typing import Generator, Any

from datek_jaipur.domain.compound_types.card import Card, CardSet
from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.compound_types.player import Player


@dataclass
class Scenario:
    name: str
    player1: Player
    player2: Player
    expected: Any


def generate_scenarios() -> Generator[Scenario, None, None]:
    camel = Card(GoodsType.CAMEL, 1)
    player1 = Player(name=_PLAYER1, score=1, goods=CardSet(), herd=CardSet([camel]))
    player2 = Player(name=_PLAYER2, score=0, goods=CardSet(), herd=CardSet())
    yield Scenario(name=_PLAYER1, player1=player1, player2=player2, expected=player1)

    player1 = Player(name=_PLAYER1, score=0, goods=CardSet(), herd=CardSet())
    player2 = Player(name=_PLAYER2, score=1, goods=CardSet(), herd=CardSet([camel]))
    yield Scenario(name=_PLAYER2, player1=player1, player2=player2, expected=player2)

    player1 = Player(name=_PLAYER1, score=1, goods=CardSet(), herd=CardSet([camel]))
    player2 = Player(name=_PLAYER2, score=1, goods=CardSet(), herd=CardSet([camel]))
    yield Scenario(name="None", player1=player1, player2=player2, expected=None)


_PLAYER1 = "Player1"
_PLAYER2 = "Player2"
