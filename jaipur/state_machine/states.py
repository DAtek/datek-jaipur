from abc import abstractmethod
from typing import Optional, Type

from datek_async_fsm.state import BaseState, StateCollection, StateType

from jaipur.compound_types.player import Player
from jaipur.compound_types.turn import TurnResultType
from jaipur.events.game_created import GameCreated
from jaipur.events.turn_completed import TurnCompleted
from jaipur.state_machine.scope import Scope


class Start(BaseState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.INITIAL

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        event = GameCreated(
            player1_name=input("Enter player 1 name: "),
            player2_name=input("Enter player 2 name: "),
        )
        event.apply()
        self.scope.game = event.result

        return states["Player1"]


class BasePlayerState(BaseState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    @staticmethod
    @abstractmethod
    def other_player_state() -> str:
        pass

    @abstractmethod
    def get_player(self) -> Player:
        pass

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        adapter = self.scope.adapter_class(
            player=self.get_player(),
            cards_on_deck=self.scope.game.cards_on_deck,
        )

        await adapter.collect_data()

        event = TurnCompleted(
            game=self.scope.game,
            type_=adapter.collected_turn_type,
            cards=adapter.collected_cards,
        )
        event.apply()
        result = event.result

        self.scope.game = result.game

        return (
            states["End"]
            if result.type is TurnResultType.WIN
            else states[self.other_player_state()]
        )


class Player1(BasePlayerState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    @staticmethod
    def other_player_state() -> str:
        return "Player2"

    def get_player(self) -> Player:
        return self.scope.game.player1


class Player2(BasePlayerState):
    scope: Scope

    @staticmethod
    def type() -> StateType:
        return StateType.STANDARD

    @staticmethod
    def other_player_state() -> str:
        return "Player1"

    def get_player(self) -> Player:
        return self.scope.game.player2


class End(BaseState):
    @staticmethod
    def type() -> StateType:
        return StateType.END

    async def transit(self, states: StateCollection) -> Optional[Type["BaseState"]]:
        pass
