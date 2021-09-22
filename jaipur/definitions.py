from enum import Enum


class GoodsType(Enum):
    DIAMOND = "Diamond"
    GOLD = "Gold"
    SILVER = "Silver"
    CLOTH = "Cloth"
    SPICE = "Spice"
    LEATHER = "Leather"
    CAMEL = "Camel"

    def __repr__(self):
        return self.value


class TurnType(Enum):
    TRADE_GOODS = "Trade goods"
    SELL_GOODS = "Sell goods"
    BUY_GOODS = "Buy goods"


CARD_AMOUNTS = {
    GoodsType.DIAMOND: 6,
    GoodsType.GOLD: 6,
    GoodsType.SILVER: 6,
    GoodsType.SPICE: 8,
    GoodsType.CLOTH: 8,
    GoodsType.LEATHER: 10,
    GoodsType.CAMEL: 11,
}

COINS = {
    GoodsType.DIAMOND: (7, 7, 5, 5, 5),
    GoodsType.GOLD: (6, 6, 5, 5, 5),
    GoodsType.SILVER: (5, 5, 5, 5, 5),
    GoodsType.CLOTH: (5, 3, 3, 2, 2, 1, 1),
    GoodsType.SPICE: (5, 3, 3, 2, 2, 1, 1),
    GoodsType.LEATHER: (4, 3, 2, 1, 1, 1, 1, 1, 1),
    GoodsType.CAMEL: (5,),
}

INITIAL_HAND_SIZE = 5
DECK_SIZE = 5
INITIALLY_NEEDED_CARDS = INITIAL_HAND_SIZE * 2 + DECK_SIZE
INITIAL_SCORE = 0

WIN_SCORE = 60
