from pytest import mark, raises

from datek_jaipur.domain.compound_types.card import CardSet, Card
from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.compound_types.player import Player
from datek_jaipur.domain.errors.goods_traded import (
    NotEnoughResourcesAtPlayerError,
    NotEnoughResourcesOnDeskError,
    GoodsCountsMismatchError,
)
from datek_jaipur.domain.events.goods_traded import GoodsTraded


class TestGoodsTraded:
    @mark.asyncio
    async def test_cant_trade_not_enough_resource(self, initial_game: Game):
        player1 = Player(
            name=initial_game.player1.name,
            goods=CardSet(),
            score=initial_game.player1.score,
            herd=initial_game.player1.herd,
        )

        game = Game(
            player1=player1,
            current_player=player1,
            player2=initial_game.player2,
            cards_on_deck=initial_game.cards_on_deck,
            cards_in_pack=initial_game.cards_in_pack,
            coins=initial_game.coins,
        )

        event = GoodsTraded(
            game=game,
            goods_to_give_away=tuple([GoodsType.GOLD]),
            goods_to_acquire=tuple([game.cards_on_deck.to_list()[0]]),
        )

        with raises(NotEnoughResourcesAtPlayerError):
            await event.apply()

    @mark.asyncio
    async def test_cant_trade_not_enough_cards_on_deck(self, initial_game: Game):
        player1 = Player(
            name=initial_game.player1.name,
            goods=CardSet([Card(GoodsType.GOLD, 1)]),
            score=initial_game.player1.score,
            herd=initial_game.player1.herd,
        )

        game = Game(
            player1=player1,
            current_player=player1,
            player2=initial_game.player2,
            cards_on_deck=CardSet(),
            cards_in_pack=initial_game.cards_in_pack,
            coins=initial_game.coins,
        )

        event = GoodsTraded(
            game=game,
            goods_to_give_away=tuple([GoodsType.GOLD]),
            goods_to_acquire=tuple([GoodsType.SILVER]),
        )

        with raises(NotEnoughResourcesOnDeskError):
            await event.apply()

    @mark.asyncio
    async def test_cant_trade_counts_mismatch(self, initial_game: Game):
        silver = Card(GoodsType.SILVER, 1)
        gold = Card(GoodsType.GOLD, 1)
        cloth = Card(GoodsType.CLOTH, 1)

        player1 = Player(
            name=initial_game.player1.name,
            goods=CardSet([gold]),
            score=initial_game.player1.score,
            herd=CardSet(),
        )

        game = Game(
            player1=player1,
            current_player=player1,
            player2=initial_game.player2,
            cards_on_deck=CardSet([silver, cloth]),
            cards_in_pack=initial_game.cards_in_pack,
            coins=initial_game.coins,
        )

        event = GoodsTraded(
            game=game,
            goods_to_give_away=tuple([gold.type]),
            goods_to_acquire=tuple([silver.type, cloth.type]),
        )

        with raises(GoodsCountsMismatchError):
            await event.apply()

    @mark.asyncio
    async def test_trade_ok(self, initial_game: Game):
        silver = Card(GoodsType.SILVER, 1)
        gold = Card(GoodsType.GOLD, 1)
        cloth = Card(GoodsType.CLOTH, 1)
        camel = Card(GoodsType.CAMEL, 1)

        player1 = Player(
            name=initial_game.player1.name,
            goods=CardSet([gold]),
            score=initial_game.player1.score,
            herd=CardSet([camel]),
        )

        game = Game(
            player1=player1,
            current_player=player1,
            player2=initial_game.player2,
            cards_on_deck=CardSet([silver, cloth]),
            cards_in_pack=initial_game.cards_in_pack,
            coins=initial_game.coins,
        )

        event = GoodsTraded(
            game=game,
            goods_to_give_away=tuple([camel.type, gold.type]),
            goods_to_acquire=tuple([silver.type, cloth.type]),
        )

        await event.apply()
        result_game = event.result

        assert result_game.player1.goods == CardSet([silver, cloth])
        assert not result_game.player1.herd
        assert result_game.current_player == game.player2
