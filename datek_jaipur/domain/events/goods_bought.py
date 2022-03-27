from datek_jaipur.domain.compound_types.card import CardSet
from datek_jaipur.domain.compound_types.game import Game
from datek_jaipur.domain.compound_types.goods import GoodsType
from datek_jaipur.domain.compound_types.player import Player
from datek_jaipur.domain.compound_types.turn import GoodsBoughtInput
from datek_jaipur.domain.constants import LARGEST_HERD_BONUS, MAX_CARDS_IN_HAND
from datek_jaipur.domain.errors.goods_bought import (
    CardNotOnDeckError,
    TooMuchCardsInHandError,
)
from datek_jaipur.domain.utils import get_herd_master, get_winner, is_game_ended
from datek_jaipur.utils import BaseEvent


class GoodsBought(BaseEvent[Game]):
    _picked_cards: CardSet
    _data_model: GoodsBoughtInput

    async def _validate(self):
        current_cards_count = len(self._data_model.game.current_player.goods)
        remaining_space = MAX_CARDS_IN_HAND - current_cards_count

        if remaining_space <= 0:
            raise TooMuchCardsInHandError

        if not (
            picked_cards := self._data_model.game.cards_on_deck.filter_by_type(
                self._data_model.goods_type
            )
        ):
            raise CardNotOnDeckError(self._data_model.goods_type)

        self._picked_cards = picked_cards

    async def _create_result(self) -> Game:
        player = self._data_model.game.current_player

        if self._data_model.goods_type == GoodsType.CAMEL:
            new_herd = player.herd + self._picked_cards
            new_goods = player.goods
        else:
            picked_card = self._picked_cards.to_list()[0]
            self._picked_cards = CardSet([picked_card])
            new_herd = player.herd
            new_goods = player.goods + self._picked_cards

        card_pack_to_deck = CardSet(
            self._data_model.game.cards_in_pack.to_list()[: len(self._picked_cards)]
            if self._data_model.game.cards_in_pack
            else CardSet()
        )

        cards_on_deck = (
            self._data_model.game.cards_on_deck - self._picked_cards + card_pack_to_deck
        )

        new_player = Player(
            name=player.name,
            score=player.score,
            goods=new_goods,
            herd=new_herd,
        )

        player1 = (
            new_player
            if self._data_model.game.player1 == new_player
            else self._data_model.game.player1
        )

        player2 = (
            new_player
            if self._data_model.game.player2 == new_player
            else self._data_model.game.player2
        )

        cards_in_pack = self._data_model.game.cards_in_pack - card_pack_to_deck

        current_player = (
            player2 if player1 == self._data_model.game.current_player else player1
        )

        if not is_game_ended(self._data_model.game.coins, cards_on_deck):
            return Game(
                player1=player1,
                player2=player2,
                current_player=current_player,
                cards_in_pack=cards_in_pack,
                cards_on_deck=cards_on_deck,
                coins=self._data_model.game.coins,
            )

        herd_master = get_herd_master(player1, player2)

        if herd_master == player1:
            player1 = Player(
                name=player1.name,
                score=player1.score + LARGEST_HERD_BONUS,
                goods=player1.goods,
                herd=player1.herd,
            )
        elif herd_master == player2:
            player2 = Player(
                name=player2.name,
                score=player2.score + LARGEST_HERD_BONUS,
                goods=player2.goods,
                herd=player2.herd,
            )

        return Game(
            player1=player1,
            player2=player2,
            current_player=current_player,
            cards_in_pack=cards_in_pack,
            cards_on_deck=cards_on_deck,
            coins=self._data_model.game.coins,
            winner=get_winner(player1, player2),
        )
