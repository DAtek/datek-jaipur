from pytest import raises

from jaipur.errors import EventAlreadyAppliedError, EventNotAppliedError
from jaipur.events.all_card_sets_created import AllCardSetsCreated


class TestBaseEvent:
    def test_apply_raises_error_when_called_twice(self):
        event = AllCardSetsCreated()
        event.apply()

        with raises(EventAlreadyAppliedError):
            event.apply()

    def test_result_raises_error_when_event_not_applied(self):
        event = AllCardSetsCreated()

        with raises(EventNotAppliedError):
            assert event.result is None
