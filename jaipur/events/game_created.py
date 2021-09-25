from random import sample

from jaipur.compound_types.card import CardSet
from jaipur.compound_types.game import Game
from jaipur.constants import (
    INITIALLY_NEEDED_CARDS,
    INITIAL_HAND_SIZE,
    DECK_SIZE,
    INITIAL_SCORE,
)
from jaipur.events.all_card_sets_created import AllCardSetsCreated
from jaipur.events.all_coin_sets_created import AllCoinSetsCreated
from jaipur.events.player_created import PlayerCreated
from jaipur.utils import BaseEvent


class GameCreated(BaseEvent[Game]):
    def __init__(self, player1_name: str, player2_name: str):
        self._player1_name = player1_name
        self._player2_name = player2_name

    def _create_result(self) -> Game:
        all_card_created = AllCardSetsCreated()
        all_card_created.apply()

        initial_cards = sample(list(all_card_created.result), INITIALLY_NEEDED_CARDS)
        hand1 = CardSet(initial_cards[:INITIAL_HAND_SIZE])
        hand2 = CardSet(initial_cards[INITIAL_HAND_SIZE : INITIAL_HAND_SIZE * 2])
        cards_on_deck = CardSet(initial_cards[-DECK_SIZE:])
        cards_in_pack = all_card_created.result - hand1 - hand2 - cards_on_deck

        player_1_created = PlayerCreated(
            name=self._player1_name, cards=hand1, score=INITIAL_SCORE
        )
        player_1_created.apply()

        player_2_created = PlayerCreated(
            name=self._player2_name, cards=hand2, score=INITIAL_SCORE
        )
        player_2_created.apply()

        coins_created = AllCoinSetsCreated()
        coins_created.apply()

        return Game(
            player1=player_1_created.result,
            player2=player_2_created.result,
            cards_on_deck=cards_on_deck,
            cards_in_pack=cards_in_pack,
            coins=coins_created.result,
            current_player=player_1_created.result,
        )
