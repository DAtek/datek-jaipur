from jaipur.compound_types.card import CardSet
from jaipur.constants import CARD_AMOUNTS, COIN_COLLECTION
from tests.events.conftest import PLAYER1, PLAYER2


class TestGameCreated:
    def test_correct_players_created(self, initial_game):
        player_names = {
            player.name for player in [initial_game.player1, initial_game.player2]
        }

        assert player_names == {PLAYER1, PLAYER2}

    def test_all_cards_created(self, initial_game):
        player_cards = CardSet(
            (
                card
                for player in [initial_game.player1, initial_game.player2]
                for card in player.cards
            )
        )

        assert sum((value for value in CARD_AMOUNTS.values())) == len(
            initial_game.cards_in_pack + initial_game.cards_on_deck + player_cards
        )

    def test_all_coins_created(self, initial_game):
        assert len(initial_game.coins) == sum(
            len(values) for values in COIN_COLLECTION.values()
        )
