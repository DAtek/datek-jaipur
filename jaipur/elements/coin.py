from jaipur.definitions import GoodsType, COINS
from jaipur.events import BaseEvent


class Coin:
    def __init__(self, type_: GoodsType, value: int, id_: int):
        self._type = type_
        self._value = value
        self._id = id_

    @property
    def type(self) -> GoodsType:
        return self._type

    @property
    def value(self) -> int:
        return self._value

    @property
    def id(self) -> int:
        return self._id

    def __repr__(self):
        return f"{self.type}: {self.value}"

    def __int__(self):
        return self._value

    def __hash__(self) -> int:
        return hash(self._type) + self._value


class CoinSet(set[Coin]):
    class CreateAll(BaseEvent["CoinSet"]):
        def _apply(self):
            type_value_tuples = (
                (type_, value)
                for type_, values in COINS.items()
                for value in values
            )

            i = 0
            result = []
            for type_, value in type_value_tuples:
                result.append(Coin(type_, value, i))
                i += 1

            self._result = CoinSet(result)

    def __sub__(self, other: "CoinSet") -> "CoinSet":
        return CoinSet(super().__sub__(other))

    @property
    def value(self) -> int:
        return sum(int(item) for item in self)

    def retrieve(self, type_: GoodsType, amount: int) -> "CoinSet":
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
