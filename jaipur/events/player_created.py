from jaipur.compound_types.card import CardSet
from jaipur.compound_types.player import Player
from jaipur.simple_types import Name, Number
from jaipur.utils import BaseEvent


class PlayerCreated(BaseEvent[Player]):
    def __init__(self, name: Name, score: Number, cards: CardSet):
        self._name = name
        self._score = score
        self._cards = cards

    def _create_result(self) -> Player:
        return Player(
            name=self._name,
            cards=self._cards,
            score=self._score,
        )
