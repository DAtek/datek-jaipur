from functools import lru_cache

from pytest import fixture

from datek_jaipur.domain.utils import get_herd_master, get_winner
from tests.domain.fixtures import Scenario, generate_scenarios


def test_get_herd_master(scenario: Scenario):
    assert get_herd_master(scenario.player1, scenario.player2) == scenario.expected


def test_get_winner(scenario: Scenario):
    assert get_winner(scenario.player1, scenario.player2) == scenario.expected


@fixture(params=(item.name for item in generate_scenarios()))
def scenario(request):
    return _scenario_map()[request.param]


@lru_cache
def _scenario_map() -> dict[str, Scenario]:
    return {item.name: item for item in generate_scenarios()}
