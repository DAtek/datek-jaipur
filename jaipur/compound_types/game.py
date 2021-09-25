from typing import NamedTuple

from jaipur.compound_types.card import CardSet
from jaipur.compound_types.coin import CoinSet
from jaipur.compound_types.player import Player

Game = NamedTuple(
    "GameFields",
    [
        ("player1", Player),
        ("player2", Player),
        ("current_player", Player),
        ("cards_in_pack", CardSet),
        ("cards_on_deck", CardSet),
        ("coins", CoinSet),
    ],
)
