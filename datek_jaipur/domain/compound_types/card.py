from dataclasses import dataclass
from typing import AbstractSet, Optional

from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.simple_types import Amount, Number


@dataclass(frozen=True)
class Card:
    type: GoodsType
    id: Number


CardList = list[Card]


class CardSet(set[Card]):
    def __add__(self, other: AbstractSet[Optional[Card]] | Card) -> "CardSet":
        if isinstance(other, CardSet):
            return CardSet(self.union(other))

        elif isinstance(other, Card):
            return CardSet(self.union(CardSet((other,))))

        raise TypeError

    def __iadd__(self, other: AbstractSet[Optional[Card]] | Card) -> "CardSet":
        return self + other

    def __sub__(self, other: AbstractSet[Optional[Card]] | Card) -> "CardSet":
        if isinstance(other, CardSet):
            return CardSet(super().__sub__(other))

        elif isinstance(other, Card):
            return CardSet(super().__sub__(CardSet((other,))))

        raise TypeError

    def __isub__(self, other: AbstractSet[Optional[Card]] | Card) -> "CardSet":
        return self - other

    def to_list(self) -> CardList:
        list_ = CardList(self)
        list_.sort(key=lambda item: item.id)
        return list_

    def filter_by_type(self, type_: GoodsType) -> "CardSet":
        return CardSet((item for item in self if item.type == type_))


@dataclass
class CardSetCreatedInput:
    type: GoodsType
    amount: Amount
