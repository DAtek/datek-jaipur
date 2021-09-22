from typing import Mapping

from jaipur.definitions import GoodsType, CARD_AMOUNTS
from jaipur.events import BaseEvent


class Card:
    def __init__(self, type_: GoodsType, id_: int):
        self._type = type_
        self._id = id_

    @property
    def type(self) -> GoodsType:
        return self._type

    @property
    def id(self) -> int:
        return self._id

    def __hash__(self) -> int:
        return hash(f"{self._type}{self._id}")

    def __repr__(self) -> str:
        return repr(self._type)


class CardSet(set[Card], Mapping):
    def __init__(self, iterable):
        super().__init__(iterable)
        self._map: dict[int, Card] = {
            item.id: item
            for item in self
        }

    def __add__(self, other: "CardSet") -> "CardSet":
        return CardSet(self.union(other))

    def __sub__(self, other: "CardSet") -> "CardSet":
        return CardSet(super().__sub__(other))

    def __getitem__(self, key) -> Card:
        return self._map[key]

    class AllCreated(BaseEvent["CardSet"]):
        def _apply(self):
            card_set_events: list[CardSet.Created] = []

            for type_, amount in CARD_AMOUNTS.items():
                event = CardSet.Created(type_, amount)
                event.apply()
                card_set_events.append(event)

            card_sets = (event.result for event in card_set_events)

            self._result = CardSet((
                card
                for card_set in card_sets
                for card in card_set
            ))

    class Created(BaseEvent["CardSet"]):
        def __init__(self, type_: GoodsType, amount: int):
            self._type = type_
            self._amount = amount

        @property
        def type(self) -> GoodsType:
            return self._type

        @property
        def amount(self) -> int:
            return self._amount

        def _apply(self):
            self._result = CardSet((
                Card(type_=self._type, id_=i)
                for i in range(self.amount)
            ))
