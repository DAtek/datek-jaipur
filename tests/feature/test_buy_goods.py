from pytest import fixture
from pytest_bdd import scenario, given, when, then

from datek_jaipur.domain.compound_types.card import CardSet, Card
from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.compound_types.player import Player
from datek_jaipur.domain.events.game_created import GameCreated
from datek_jaipur.domain.events.goods_bought import GoodsBought


@scenario("buy_goods.feature", "Buying a diamond")
def test_buy_diamond(game):
    pass


@given("I have less then 7 cards", target_fixture="game")
def me(game) -> Game:
    me = Player(
        name=game.player1.name,
        score=game.player1.score,
        goods=CardSet(),
        herd=game.player1.herd,
    )

    return Game(
        player1=me,
        player2=game.player2,
        current_player=game.current_player,
        cards_on_deck=game.cards_on_deck,
        cards_in_pack=game.cards_in_pack,
        coins=game.coins,
    )


@given("A diamond is among the cards in the deck", target_fixture="game")
def cards_on_deck(game, diamond_card):
    return Game(
        player1=game.player1,
        player2=game.player2,
        current_player=game.current_player,
        cards_on_deck=CardSet([diamond_card]),
        cards_in_pack=game.cards_in_pack,
        coins=game.coins,
    )


@given("It's my turn", target_fixture="game")
def my_turn(game):
    return Game(
        player1=game.player1,
        player2=game.player2,
        current_player=game.player1,
        cards_on_deck=game.cards_on_deck,
        cards_in_pack=game.cards_in_pack,
        coins=game.coins,
    )


@when("I pick a diamond card", target_fixture="game")
def pick_diamond(game, event_loop):
    event = GoodsBought(game=game, goods_type=GoodsType.DIAMOND)

    event_loop.run_until_complete(event.apply())

    return event.result


@then("I should see the bought diamond in my hand")
def i_got_a_diamond(game, diamond_card):
    assert game.player1.goods == CardSet([diamond_card])


@fixture
def game(player1, player2, event_loop) -> Game:
    event = GameCreated(
        player1_name=player1,
        player2_name=player2,
    )

    event_loop.run_until_complete(event.apply())

    return event.result


@fixture
def diamond_card() -> Card:
    return Card(type=GoodsType.DIAMOND, id=1)


@fixture
def player1() -> str:
    return "player1"


@fixture
def player2() -> str:
    return "player2"
