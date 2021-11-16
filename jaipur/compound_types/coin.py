from dataclasses import dataclass

from jaipur.compound_types.goods import GoodsType
from jaipur.simple_types import Number, Amount


@dataclass(frozen=True)
class Coin:
    type: GoodsType
    value: Number
    id: Number

    def __repr__(self):
        return f"{self.type}: {self.value}"

    def __int__(self):
        return self.value


class CoinSet(set[Coin]):
    def __sub__(self, other: "CoinSet") -> "CoinSet":
        return CoinSet(super().__sub__(other))

    @property
    def value(self) -> Number:
        return sum(Number(item) for item in self)

    def retrieve(self, type_: GoodsType, amount: Amount) -> "CoinSet":
        sorted_coins = sorted(
            (item for item in self if item.type == type_),
            key=lambda item: item.value,
            reverse=True
        )

        return CoinSet(sorted_coins[:amount])
