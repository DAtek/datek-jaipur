from dataclasses import dataclass

from pytest import mark

from jaipur.compound_types.card import CardSet, Card
from jaipur.compound_types.game import Game
from jaipur.compound_types.goods import GoodsType
from jaipur.compound_types.player import Player
from jaipur.compound_types.turn import TurnType, TurnResultType
from jaipur.constants import COIN_COLLECTION, WIN_SCORE
from jaipur.events.turn_completed import TurnCompleted


@dataclass
class TurnScenario:
    cards: CardSet
    expected_score: int

    @classmethod
    def create(
        cls,
        card_type: GoodsType,
        amount: int,
        expected_score: int,
    ) -> "TurnScenario":
        cards = CardSet((Card(card_type, i) for i in range(amount)))

        return cls(cards, expected_score)


class TestTurnCompleted:
    @mark.parametrize(
        "scenario",
        [
            TurnScenario.create(GoodsType.GOLD, 2, 12),
            TurnScenario.create(GoodsType.GOLD, 3, 17),
            TurnScenario.create(GoodsType.SPICE, 1, 5),
        ],
        ids=["gold1", "gold2", "spice"],
    )
    def test_sell_goods(self, initial_game, scenario: TurnScenario):
        player1 = Player(
            name=initial_game.player1.name,
            score=0,
            cards=CardSet(
                (
                    Card(GoodsType.GOLD, 1),
                    Card(GoodsType.GOLD, 2),
                )
            ),
        )

        game = _create_modified_game(
            game=initial_game, player1=player1, current_player=player1
        )

        event = TurnCompleted(
            game=game, type_=TurnType.SELL_GOODS, cards=game.player1.cards
        )
        event.apply()
        new_game = event.result.game

        assert new_game.player1.score == sum(COIN_COLLECTION[GoodsType.GOLD][:2])
        assert not new_game.player1.cards
        assert new_game.current_player is initial_game.player2
        assert event.result.type is TurnResultType.NEXT

    def test_player_won(self, initial_game):
        player1 = Player(
            name=initial_game.player1.name,
            score=WIN_SCORE - 1,
            cards=CardSet((Card(GoodsType.SPICE, 1),)),
        )

        game = _create_modified_game(
            game=initial_game, player1=player1, current_player=player1
        )

        event = TurnCompleted(
            game=game, type_=TurnType.SELL_GOODS, cards=initial_game.player1.cards
        )
        event.apply()

        new_game = event.result.game

        assert event.result.type is TurnResultType.WIN
        assert new_game.current_player is initial_game.player2

    def test_buy_goods(self, initial_game):
        player1 = Player(name=initial_game.player1.name, score=0, cards=CardSet([]))

        chosen_card = list(initial_game.cards_on_deck)[0]

        game = _create_modified_game(
            game=initial_game, player1=player1, current_player=player1
        )

        event = TurnCompleted(
            game=game, type_=TurnType.BUY_GOODS, cards=CardSet([chosen_card])
        )

        event.apply()
        new_game = event.result.game

        assert chosen_card in new_game.player1.cards
        assert chosen_card not in new_game.cards_on_deck
        assert chosen_card not in new_game.cards_in_pack
        assert new_game.current_player is initial_game.player2
        assert event.result.type is TurnResultType.NEXT


def _create_modified_game(**kwargs) -> Game:
    game: Game = kwargs.get("game")

    params = {
        key: kwargs.get(key) or getattr(game, key)
        for key in [
            "player1",
            "player2",
            "current_player",
            "cards_in_pack",
            "cards_on_deck",
            "coins",
        ]
    }

    return Game(**params)
