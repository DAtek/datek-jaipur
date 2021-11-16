from dataclasses import dataclass

from jaipur.compound_types.goods import GoodsType
from jaipur.simple_types import Number, Name


@dataclass(frozen=True)
class Card:
    type: GoodsType
    id: Number

    def __repr__(self) -> Name:
        return repr(self.type)

    def __str__(self) -> Name:
        return Name(self.type)


CardList = list[Card]


class CardSet(set[Card]):
    def __add__(self, other: "CardSet") -> "CardSet":
        return CardSet(self.union(other))

    def __sub__(self, other: "CardSet") -> "CardSet":
        return CardSet(super().__sub__(other))

    def __str__(self) -> Name:
        return ", ".join((Name(item) for item in self))

    def to_list(self) -> CardList:
        return CardList(self)
