from typing import NamedTuple

from jaipur.compound_types.card import CardSet
from jaipur.simple_types import Name, Number


PlayerFields = NamedTuple(
    "PlayerFields",
    [
        ("name", Name),
        ("score", Number),
        ("cards", CardSet),
    ],
)


class Player(PlayerFields):
    def __hash__(self) -> Number:
        return hash(self.name)

    def __eq__(self, other: "Player"):
        return hash(self) == hash(other)


PlayerCollection = NamedTuple(
    "PlayerCollection",
    [
        ("player1", Player),
        ("player2", Player),
        ("current_player", Player),
    ],
)
