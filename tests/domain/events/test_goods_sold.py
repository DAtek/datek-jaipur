from pytest import mark, raises

from datek_jaipur.domain.compound_types.card import CardSet, Card
from datek_jaipur.domain.compound_types.coin import CoinSet, Coin
from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.compound_types.player import Player
from datek_jaipur.domain.constants import (
    BONUS_FOR_3_MIN,
    BONUS_FOR_3_MAX,
    LARGEST_HERD_BONUS,
)
from datek_jaipur.domain.errors.goods_sold import NotEnoughCardsError
from datek_jaipur.domain.events.goods_sold import GoodsSold


class TestGoodsSold:
    @mark.asyncio
    async def test_not_enough_cards(self, initial_game: Game):
        player1 = Player(
            name=initial_game.player1.name, score=0, goods=CardSet(), herd=CardSet()
        )

        game = Game(
            player1=player1,
            player2=initial_game.player2,
            current_player=player1,
            cards_in_pack=initial_game.cards_in_pack,
            cards_on_deck=initial_game.cards_on_deck,
            coins=initial_game.coins,
        )

        event = GoodsSold(game=game, goods_type=GoodsType.DIAMOND)

        with raises(NotEnoughCardsError):
            await event.apply()

    @mark.asyncio
    async def test_game_ended(self, initial_game: Game):
        goods_type = GoodsType.DIAMOND
        card1 = Card(type=goods_type, id=1)
        card2 = Card(type=goods_type, id=2)
        card3 = Card(type=goods_type, id=3)
        camel_card = Card(type=GoodsType.CAMEL, id=1)
        cards_to_sell = CardSet((card1, card2, card3))
        coins = CoinSet(
            (
                Coin(GoodsType.DIAMOND, 7, 1),
                Coin(GoodsType.DIAMOND, 7, 2),
                Coin(GoodsType.DIAMOND, 7, 5),
                Coin(GoodsType.GOLD, 1, 3),
                Coin(GoodsType.SPICE, 1, 4),
                Coin(GoodsType.SILVER, 1, 4),
            )
        )

        initial_player_score = 1

        player1 = Player(
            name=initial_game.player1.name,
            score=initial_player_score,
            goods=cards_to_sell,
            herd=CardSet([camel_card]),
        )

        player2 = Player(
            name=initial_game.player2.name,
            score=initial_player_score,
            goods=initial_game.player2.goods,
            herd=CardSet(),
        )

        game = Game(
            player1=player1,
            player2=player2,
            current_player=player1,
            cards_in_pack=initial_game.cards_in_pack,
            cards_on_deck=initial_game.cards_on_deck,
            coins=coins,
        )

        event = GoodsSold(game=game, goods_type=goods_type)

        await event.apply()

        sold_coins = game.coins.retrieve(goods_type, len(cards_to_sell))
        result_game = event.result

        assert (
            result_game.player1.score
            >= sold_coins.value
            + initial_player_score
            + BONUS_FOR_3_MIN
            + LARGEST_HERD_BONUS
        )

        assert (
            result_game.player1.score
            <= sold_coins.value
            + initial_player_score
            + BONUS_FOR_3_MAX
            + LARGEST_HERD_BONUS
        )

        assert result_game.coins == game.coins - sold_coins
        assert result_game.winner == player1
