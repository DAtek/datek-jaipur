from pytest import raises, mark

from datek_jaipur.errors import EventAlreadyAppliedError, EventNotAppliedError
from datek_jaipur.domain.events.all_card_sets_created import AllCardSetsCreated


class TestBaseEvent:
    @mark.asyncio
    async def test_apply_raises_error_when_called_twice(self):
        event = AllCardSetsCreated()
        await event.apply()

        with raises(EventAlreadyAppliedError):
            await event.apply()

    @mark.asyncio
    async def test_result_raises_error_when_event_not_applied(self):
        event = AllCardSetsCreated()

        with raises(EventNotAppliedError):
            assert event.result is None
