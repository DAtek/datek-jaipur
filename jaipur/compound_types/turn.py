from enum import Enum
from typing import NamedTuple

from jaipur.compound_types.game import Game


class Turn(Enum):
    TRADE_GOODS = "Trade goods"
    SELL_GOODS = "Sell goods"
    BUY_GOODS = "Buy goods"


class TurnType(Enum):
    TRADE_GOODS = "Trade goods"
    SELL_GOODS = "Sell goods"
    BUY_GOODS = "Buy goods"


class TurnResultType(Enum):
    NEXT = "Next"
    WIN = "Winner"


TurnResult = NamedTuple(
    "TurnResult",
    [
        ("type", TurnResultType),
        ("game", Game),
    ],
)
