from dataclasses import dataclass

from jaipur.compound_types.card import CardSet
from jaipur.simple_types import Name, Number


@dataclass(frozen=True)
class Player:
    name: Name
    score: Number
    cards: CardSet

    def __hash__(self) -> Number:
        return hash(self.name)

    def __eq__(self, other: "Player"):
        return hash(self) == hash(other)

    def __str__(self) -> Name:
        return self.name


@dataclass(frozen=True)
class PlayerCollection:
    player1: Player
    player2: Player
    current_player: Player
