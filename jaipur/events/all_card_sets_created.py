from jaipur.compound_types.card import CardSet
from jaipur.constants import CARD_AMOUNTS
from jaipur.events.card_set_created import CardSetCreated
from jaipur.utils import BaseEvent


class AllCardSetsCreated(BaseEvent[CardSet]):
    def _create_result(self) -> CardSet:
        card_set_events: list[CardSetCreated] = []

        for type_, amount in CARD_AMOUNTS.items():
            event = CardSetCreated(type_, amount)
            event.apply()
            card_set_events.append(event)

        card_sets = (event.result for event in card_set_events)

        return CardSet((card for card_set in card_sets for card in card_set))
