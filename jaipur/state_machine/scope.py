from dataclasses import dataclass
from typing import Type

from jaipur.adapters.base import BaseAdapter
from jaipur.compound_types.game import Game


@dataclass
class Scope:
    adapter_class: Type[BaseAdapter]
    game: Game = None
