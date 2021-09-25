from jaipur.compound_types.card import CardSet
from jaipur.compound_types.game import Game
from jaipur.compound_types.player import Player, PlayerCollection
from jaipur.compound_types.turn import TurnResult, TurnType, TurnResultType
from jaipur.constants import WIN_SCORE
from jaipur.utils import BaseEvent, Result


class TurnCompleted(BaseEvent[TurnResult]):
    def __init__(self, game: Game, type_: TurnType, cards: CardSet):
        self._game = game
        self._type = type_
        self._cards = cards

        self._move_type_result_map = {
            TurnType.SELL_GOODS: self._sell_goods,
            TurnType.BUY_GOODS: self._buy_goods,
        }

    def _create_result(self) -> Result:
        method = self._move_type_result_map[self._type]
        return method()

    def _sell_goods(self) -> TurnResult:
        cards_list = self._cards.to_list()

        retrieved_coins = self._game.coins.retrieve(
            type_=cards_list[0].type,
            amount=len(cards_list),
        )

        new_score = self._game.current_player.score + retrieved_coins.value
        remaining_cards = self._game.current_player.cards - self._cards

        current_player = Player(
            name=self._game.current_player.name, score=new_score, cards=remaining_cards
        )

        all_players = self._get_all_players(current_player)

        game = Game(
            player1=all_players.player1,
            player2=all_players.player2,
            current_player=all_players.current_player,
            cards_on_deck=self._game.cards_on_deck,
            cards_in_pack=self._game.cards_in_pack,
            coins=self._game.coins - retrieved_coins,
        )

        result_type = (
            TurnResultType.WIN if new_score >= WIN_SCORE else TurnResultType.NEXT
        )

        return TurnResult(result_type, game)

    def _buy_goods(self) -> TurnResult:
        new_player_cards = self._game.current_player.cards + self._cards
        new_cards_on_deck = self._game.cards_on_deck - self._cards

        next_card_set = CardSet(
            [self._game.cards_in_pack.pop() for _ in range(len(self._cards))]
        )
        new_cards_on_deck += next_card_set
        new_cards_in_pack = self._game.cards_in_pack - next_card_set

        current_player = Player(
            name=self._game.current_player.name,
            score=self._game.current_player.score,
            cards=new_player_cards,
        )

        all_players = self._get_all_players(current_player)

        game = Game(
            player1=all_players.player1,
            player2=all_players.player2,
            current_player=all_players.current_player,
            cards_in_pack=new_cards_in_pack,
            cards_on_deck=new_cards_on_deck,
            coins=self._game.coins,
        )

        return TurnResult(TurnResultType.NEXT, game)

    def _get_all_players(self, current_player: Player) -> PlayerCollection:
        if current_player == self._game.player1:
            return PlayerCollection(
                player1=current_player,
                player2=self._game.player2,
                current_player=self._game.player2,
            )

        return PlayerCollection(
            player1=self._game.player1,
            player2=current_player,
            current_player=self._game.player1,
        )
