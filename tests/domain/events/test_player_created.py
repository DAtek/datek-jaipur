from pytest import raises, mark

from datek_jaipur.domain.compound_types.card import CardSet
from datek_jaipur.domain.errors.player_created import InvalidNameError
from datek_jaipur.domain.events.player_created import PlayerCreated


class TestPlayerCreated:
    @mark.asyncio
    async def test_cant_create_with_empty_name(self):
        event = PlayerCreated(
            name="    ",
            score=0,
            goods=CardSet(),
            herd=CardSet(),
        )
        with raises(InvalidNameError):
            await event.apply()
