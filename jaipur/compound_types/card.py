from typing import NamedTuple

from jaipur.compound_types.goods import GoodsType
from jaipur.simple_types import Number, Name

CardFields = NamedTuple(
    "CardFields",
    [
        ("type", GoodsType),
        ("id", Number),
    ],
)


class Card(CardFields):
    def __repr__(self) -> Name:
        return repr(self.type)


CardList = list[Card]


class CardSet(set[Card]):
    def __init__(self, iterable):
        super().__init__(iterable)
        self._map: dict[Number, Card] = {item.id: item for item in self}

    def __add__(self, other: "CardSet") -> "CardSet":
        return CardSet(self.union(other))

    def __sub__(self, other: "CardSet") -> "CardSet":
        return CardSet(super().__sub__(other))

    def to_list(self) -> CardList:
        return CardList(self)
