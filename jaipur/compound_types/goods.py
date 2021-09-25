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
