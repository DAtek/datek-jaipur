from pytest import mark, raises

from datek_jaipur.domain.compound_types.card import CardSet
from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.constants import CARD_AMOUNTS, COIN_COLLECTION
from datek_jaipur.domain.errors.game_created import PlayerNamesAreSameError
from datek_jaipur.domain.events.game_created import GameCreated
from tests.unit.domain.events.conftest import PLAYER1, PLAYER2


class TestGameCreated:
    @mark.asyncio
    async def test_correct_players_created(self, initial_game: Game):
        player_names = {
            player.name for player in [initial_game.player1, initial_game.player2]
        }

        assert player_names == {PLAYER1, PLAYER2}

    @mark.asyncio
    async def test_all_cards_created(self, initial_game: Game):
        player_cards = CardSet(
            card
            for player in [initial_game.player1, initial_game.player2]
            for card in player.goods
        )

        player_herds = CardSet(
            card
            for player in [initial_game.player1, initial_game.player2]
            for card in player.herd
        )

        assert sum(value for value in CARD_AMOUNTS.values()) == len(
            initial_game.cards_in_pack
            + initial_game.cards_on_deck
            + player_cards
            + player_herds
        )

    @mark.asyncio
    async def test_all_coins_created(self, initial_game: Game):
        assert len(initial_game.coins) == sum(
            len(values) for values in COIN_COLLECTION.values()
        )

    @mark.asyncio
    async def test_cant_create_with_same_player_names(self, initial_game: Game):
        event = GameCreated(
            player1_name="a",
            player2_name="a",
        )

        with raises(PlayerNamesAreSameError):
            await event.apply()
