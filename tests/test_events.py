from jaipur.elements.card import CardSet
from pytest import raises

from jaipur.errors import EventAlreadyAppliedError


class TestBaseEvent:
    def test_apply_raises_error_when_called_twice(self):
        event = CardSet.AllCreated()
        event.apply()

        with raises(EventAlreadyAppliedError):
            event.apply()
