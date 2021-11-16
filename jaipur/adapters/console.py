from enum import Enum

from jaipur.adapters.base import BaseAdapter
from jaipur.compound_types.card import CardSet
from jaipur.compound_types.turn import TurnType
from jaipur.utils import run_in_thread_pool


class ConsoleTurnType(Enum):
    S = TurnType.SELL_GOODS
    B = TurnType.BUY_GOODS
    T = TurnType.TRADE_GOODS

    @classmethod
    def _missing_(cls, value):
        for item in cls:
            if item.name == value:
                return item


class ConsoleAdapter(BaseAdapter):
    async def collect_data(self):
        print(f"{self._player}, it's your turn")
        Color.BLUE.print(f"Your cards: {self._player.cards}")
        print(f"Cards on deck: {self._cards_on_deck}")

        turn_type: str = await run_in_thread_pool(
            input, "Pick your action: (S)ell, (B)uy, (T)rade: "
        )
        print()

        console_turn_type: ConsoleTurnType = ConsoleTurnType(turn_type)
        self._collected_turn_type = console_turn_type.value
        cards_input: str = await run_in_thread_pool(input, "Select your cards: ")

        card_names = cards_input.strip().split(",")
        self._collected_cards = get_cards_from_string_list(
            card_names, self._player.cards
        )


class Color(Enum):
    WHITE = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    ORANGE = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"

    def print(self, value):
        print(f"{self.value}{value}{self.WHITE.value}")


def get_cards_from_string_list(names: list[str], cards: CardSet):
    selected_cards = []

    for item in names:
        for card in cards:
            if str(card.type) == item:
                selected_cards.append(card)
                break

    return CardSet(selected_cards)
