from typing import NamedTuple

from jaipur.compound_types.goods import GoodsType
from jaipur.simple_types import Number, Amount


CoinFields = NamedTuple(
    "CoinFields",
    [
        ("type", GoodsType),
        ("value", Number),
        ("id", Number),
    ],
)


class Coin(CoinFields):
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
        coins = []
        sorted_coins = sorted(self, key=lambda item: item.value, reverse=True)

        for item_ in sorted_coins:
            if item_.type != type_:
                continue

            coins.append(item_)
            if len(coins) == amount:
                break

        coins = CoinSet(coins)
        return coins
