from dataclasses import dataclass
from enum import Enum
from random import sample

from jaipur.definitions import (
    INITIALLY_NEEDED_CARDS,
    INITIAL_HAND_SIZE,
    DECK_SIZE,
    INITIAL_SCORE,
    GoodsType,
    TurnType,
    WIN_SCORE,
)
from jaipur.elements.card import CardSet, Card
from jaipur.elements.coin import CoinSet
from jaipur.elements.player import Player
from jaipur.events import BaseEvent


class TurnResultType(Enum):
    NEXT = "Next"
    WIN = "Winner"


class TurnResult:
    def __init__(self, type_: TurnResultType, game: "Game"):
        self._type = type_
        self._game = game

    @property
    def type(self) -> TurnResultType:
        return self._type

    @property
    def game(self) -> "Game":
        return self._game


class Game:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        current_player: Player,
        cards_in_pack: CardSet,
        cards_on_deck: CardSet,
        coins: CoinSet,
    ):
        self._player1 = player1
        self._player2 = player2
        self._current_player = current_player
        self._cards_in_pack = cards_in_pack
        self._cards_on_deck = cards_on_deck
        self._coins = coins

    @property
    def player1(self) -> Player:
        return self._player1

    @property
    def player2(self) -> Player:
        return self._player2

    @property
    def current_player(self) -> Player:
        return self._current_player

    @property
    def cards_in_pack(self) -> CardSet:
        return self._cards_in_pack

    @property
    def cards_on_deck(self) -> CardSet:
        return self._cards_on_deck

    @property
    def coins(self) -> CoinSet:
        return self._coins

    class Created(BaseEvent["Game"]):
        def __init__(self, player1_name: str, player2_name: str):
            self._player1_name = player1_name
            self._player2_name = player2_name

        def _apply(self):
            all_card_created = CardSet.AllCreated()
            all_card_created.apply()

            initial_cards = sample(list(all_card_created.result), INITIALLY_NEEDED_CARDS)
            hand1 = CardSet(initial_cards[:INITIAL_HAND_SIZE])
            hand2 = CardSet(initial_cards[INITIAL_HAND_SIZE: INITIAL_HAND_SIZE * 2])
            cards_on_deck = CardSet(initial_cards[-DECK_SIZE:])
            cards_in_pack = all_card_created.result - hand1 - hand2 - cards_on_deck

            player_1_created = Player.Created(
                name=self._player1_name,
                cards=hand1,
                score=INITIAL_SCORE
            )
            player_1_created.apply()

            player_2_created = Player.Created(
                name=self._player2_name,
                cards=hand2,
                score=INITIAL_SCORE
            )
            player_2_created.apply()

            coins_created = CoinSet.CreateAll()
            coins_created.apply()
            self._result = Game(
                player1=player_1_created.result,
                player2=player_2_created.result,
                cards_on_deck=cards_on_deck,
                cards_in_pack=cards_in_pack,
                coins=coins_created.result,
                current_player=player_1_created.result,
            )

    class TurnCompleted(BaseEvent[TurnResult]):
        def __init__(self, game: "Game", type_: TurnType, cards: CardSet):
            self._game = game
            self._type = type_
            self._cards = cards

            self._move_type_action_map = {
                TurnType.SELL_GOODS: self._sell_goods,
                TurnType.BUY_GOODS: self._buy_goods,
            }

        def _apply(self):
            method = self._move_type_action_map[self._type]
            self._result = method()

        def _sell_goods(self) -> TurnResult:
            cards_list: list[Card] = list(self._cards)

            coins = self._game.retrieve_coins(
                type_=cards_list[0].type,
                amount=len(cards_list)
            )

            new_score = self._game.current_player.score + coins.value
            remaining_cards = self._game.current_player.cards - self._cards

            current_player = Player(
                name=self._game.current_player.name,
                score=new_score,
                cards=remaining_cards
            )

            all_players = self._get_all_players(current_player)

            game = Game(
                player1=all_players.player1,
                player2=all_players.player2,
                current_player=all_players.current_player,
                cards_on_deck=self._game.cards_on_deck,
                cards_in_pack=self._game.cards_in_pack,
                coins=self._game.coins - coins
            )

            result_type = TurnResultType.WIN \
                if new_score >= WIN_SCORE \
                else TurnResultType.NEXT

            return TurnResult(result_type, game)

        def _buy_goods(self) -> TurnResult:
            new_player_cards = self._game.current_player.cards + self._cards
            new_cards_on_deck = self._game.cards_on_deck - self._cards

            next_card_set = CardSet([self._game.cards_in_pack.pop() for _ in range(len(self._cards))])
            new_cards_on_deck += next_card_set
            new_cards_in_pack = self._game.cards_in_pack - next_card_set

            current_player = Player(
                name=self._game.current_player.name,
                score=self._game.current_player.score,
                cards=new_player_cards
            )

            all_players = self._get_all_players(current_player)

            game = Game(
                player1=all_players.player1,
                player2=all_players.player2,
                current_player=all_players.current_player,
                cards_in_pack=new_cards_in_pack,
                cards_on_deck=new_cards_on_deck,
                coins=self._game.coins
            )

            return TurnResult(TurnResultType.NEXT, game)

        def _get_all_players(self, current_player: Player) -> "_PlayerCollection":
            if current_player == self._game.player1:
                return _PlayerCollection(
                    player1=current_player,
                    player2=self._game.player2,
                    current_player=self._game.player2
                )

            return _PlayerCollection(
                player1=self._game.player1,
                player2=current_player,
                current_player=self._game.player1
            )

    def retrieve_coins(self, type_: GoodsType, amount: int) -> CoinSet:
        wanted_coins = self.coins.retrieve(type_, amount)
        self._coins -= wanted_coins
        return wanted_coins


@dataclass
class _PlayerCollection:
    current_player: Player
    player1: Player
    player2: Player