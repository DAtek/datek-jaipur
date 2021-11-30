from pytest import mark, raises

from datek_jaipur.domain.compound_types.card import CardSet, Card
from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.compound_types.player import Player
from datek_jaipur.domain.constants import (
    MAX_CARDS_IN_HAND,
    LARGEST_HERD_BONUS,
    DECK_SIZE,
)
from datek_jaipur.domain.errors.goods_bought import (
    TooMuchCardsInHandError,
    CardNotOnDeckError,
)
from datek_jaipur.domain.events.goods_bought import GoodsBought


class TestGoodsBought:
    @mark.asyncio
    async def test_too_much_cards_in_hand(self, initial_game: Game):
        game = initial_game
        current_card_number = len(initial_game.player1.goods)
        remaining_slots = MAX_CARDS_IN_HAND - current_card_number

        async def buy(game_: Game) -> Game:
            suitable_cards = game_.cards_on_deck - game_.cards_on_deck.filter_by_type(
                GoodsType.CAMEL
            )
            picked_card = suitable_cards.to_list()[0]
            event = GoodsBought(game=game_, goods_type=picked_card.type)
            await event.apply()
            return Game(
                player1=event.result.player1,
                player2=event.result.player2,
                current_player=event.result.player1,
                cards_in_pack=event.result.cards_in_pack,
                cards_on_deck=event.result.cards_on_deck,
                coins=event.result.coins,
                winner=event.result.winner,
            )

        for _ in range(remaining_slots):
            game = await buy(game)

        with raises(TooMuchCardsInHandError):
            await buy(game)

    @mark.asyncio
    async def test_card_not_in_deck(self, initial_game: Game):
        player1 = Player(
            name=initial_game.player1.name, score=0, goods=CardSet(), herd=CardSet()
        )

        game = Game(
            player1=player1,
            player2=initial_game.player2,
            current_player=player1,
            cards_in_pack=initial_game.cards_in_pack,
            cards_on_deck=CardSet(),
            coins=initial_game.coins,
        )

        event = GoodsBought(game=game, goods_type=GoodsType.DIAMOND)

        with raises(CardNotOnDeckError):
            await event.apply()

    @mark.asyncio
    async def test_ok_not_camel(self, initial_game: Game):
        player1 = Player(
            name=initial_game.player1.name, score=0, goods=CardSet(), herd=CardSet()
        )

        cards_on_deck_without_camels = (
            initial_game.cards_on_deck
            - initial_game.cards_on_deck.filter_by_type(GoodsType.CAMEL)
        )

        cards_in_pack = initial_game.cards_in_pack
        i = -1
        while len(cards_on_deck_without_camels) != DECK_SIZE:
            i += 1
            picked_card = cards_in_pack.to_list()[i]
            if picked_card.type == GoodsType.CAMEL:
                continue
            cards_in_pack -= picked_card
            cards_on_deck_without_camels += picked_card

        game = Game(
            player1=player1,
            player2=initial_game.player2,
            current_player=player1,
            cards_in_pack=cards_in_pack,
            cards_on_deck=cards_on_deck_without_camels,
            coins=initial_game.coins,
        )
        picked_card = cards_on_deck_without_camels.to_list()[0]
        event = GoodsBought(game=game, goods_type=picked_card.type)

        await event.apply()
        assert event.result.player1.goods == CardSet([picked_card])
        assert len(event.result.cards_on_deck) == DECK_SIZE
        assert len(event.result.cards_in_pack) == len(cards_in_pack) - 1
        assert picked_card not in event.result.cards_on_deck

    @mark.asyncio
    async def test_all_camels_bought_from_deck(self, initial_game: Game):
        player1 = Player(
            name=initial_game.player1.name, score=0, goods=CardSet(), herd=CardSet()
        )

        cards_in_pack = initial_game.cards_in_pack
        herd = CardSet([Card(GoodsType.CAMEL, 1), Card(GoodsType.CAMEL, 2)])
        cards_on_deck = CardSet(herd)
        i = -1
        while len(cards_on_deck) != DECK_SIZE:
            i += 1
            picked_card = cards_in_pack.to_list()[i]
            if picked_card.type == GoodsType.CAMEL:
                continue
            cards_in_pack -= picked_card
            cards_on_deck += picked_card

        game = Game(
            player1=player1,
            player2=initial_game.player2,
            current_player=player1,
            cards_in_pack=cards_in_pack,
            cards_on_deck=cards_on_deck,
            coins=initial_game.coins,
        )

        event = GoodsBought(game=game, goods_type=GoodsType.CAMEL)

        await event.apply()
        assert event.result.player1.herd == herd
        assert len(event.result.cards_on_deck) == DECK_SIZE
        assert len(event.result.cards_in_pack) == len(cards_in_pack) - len(herd)

    @mark.asyncio
    async def test_game_ended(self, initial_game: Game):
        initial_player_score = 1

        player1 = Player(
            name=initial_game.player1.name,
            score=initial_player_score,
            goods=CardSet(),
            herd=CardSet([Card(GoodsType.CAMEL, id=1)]),
        )

        player2 = Player(
            name=initial_game.player2.name,
            score=initial_game.player2.score,
            goods=CardSet(),
            herd=CardSet(),
        )

        cards_in_pack = CardSet()

        gold_card = Card(
            type=GoodsType.GOLD,
            id=1,
        )

        game = Game(
            player1=player1,
            player2=player2,
            current_player=player1,
            cards_in_pack=cards_in_pack,
            cards_on_deck=CardSet([gold_card]),
            coins=initial_game.coins,
        )

        event = GoodsBought(game=game, goods_type=gold_card.type)

        await event.apply()
        result_game = event.result

        assert event.result.player1.goods == CardSet([gold_card])
        assert not len(event.result.cards_on_deck)
        assert not len(event.result.cards_in_pack)
        assert gold_card not in event.result.cards_on_deck
        assert event.result.winner == player1

        assert result_game.player1.score == initial_player_score + LARGEST_HERD_BONUS
