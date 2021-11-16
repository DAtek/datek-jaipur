from dataclasses import dataclass
from enum import Enum

from jaipur.compound_types.game import Game


class TurnType(Enum):
    TRADE_GOODS = "Trade goods"
    SELL_GOODS = "Sell goods"
    BUY_GOODS = "Buy goods"


class TurnResultType(Enum):
    NEXT = "Next"
    WIN = "Winner"


@dataclass(frozen=True)
class TurnResult:
    type: TurnResultType
    game: Game
