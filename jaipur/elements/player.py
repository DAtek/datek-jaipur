from jaipur.elements.card import CardSet
from jaipur.events import BaseEvent


class Player:
    def __init__(self, name: str, score: int, cards: CardSet):
        self._name = name
        self._score = score
        self._cards = cards

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> int:
        return self._score

    @property
    def cards(self) -> CardSet:
        return self._cards

    def __hash__(self) -> int:
        return hash(self._name)

    def __eq__(self, other: "Player"):
        return hash(self) == hash(other)

    class Created(BaseEvent["Player"]):
        def __init__(self, name: str, score: int, cards: CardSet):
            self._name = name
            self._score = score
            self._cards = cards

        def _apply(self):
            self._result = Player(
                name=self._name,
                cards=self._cards,
                score=self._score,
            )
