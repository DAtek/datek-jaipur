from jaipur.compound_types.card import CardSet, Card
from jaipur.compound_types.goods import GoodsType
from jaipur.utils import BaseEvent


class CardSetCreated(BaseEvent[CardSet]):
    def __init__(self, type_: GoodsType, amount: int):
        self._type = type_
        self._amount = amount

    def _create_result(self) -> CardSet:
        return CardSet((Card(type=self._type, id=i) for i in range(self._amount)))
