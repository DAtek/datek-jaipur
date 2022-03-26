from pytest import raises

from datek_jaipur.domain.compound_types.card import Card, CardSet
from datek_jaipur.domain.compound_types.goods import GoodsType


class TestCard:
    def test_add_raises_type_error_with_wrong_type(self):
        with raises(TypeError):
            (
                CardSet(
                    [
                        Card(
                            type=GoodsType.CAMEL,
                            id=1,
                        )
                    ]
                )
                + {GoodsType.CAMEL}
            )

    def test_sub_raises_type_error_with_wrong_type(self):
        with raises(TypeError):
            (
                CardSet(
                    [
                        Card(
                            type=GoodsType.CAMEL,
                            id=1,
                        )
                    ]
                )
                - {GoodsType.CAMEL}
            )
