from abc import abstractmethod

from jaipur.compound_types.card import CardSet
from jaipur.compound_types.player import Player
from jaipur.compound_types.turn import TurnType
from jaipur.errors import DataNotCollectedError
import os


class BaseAdapter:
    def __init__(self, player: Player, cards_on_deck: CardSet):
        self._player = player
        self._cards_on_deck = cards_on_deck
        self._collected_cards: CardSet = ...
        self._collected_turn_type: TurnType = ...

    @property
    def collected_cards(self) -> CardSet:
        if self._collected_cards is ...:
            raise DataNotCollectedError

        return self._collected_cards

    @property
    def collected_turn_type(self) -> TurnType:
        if self._collected_turn_type is ...:
            raise DataNotCollectedError

        return self._collected_turn_type

    @abstractmethod
    async def collect_data(self):
        pass
