"""Fixture to load batterie discharging above reserve responses
    using all sync methods called from async tests using asyncio.run_in_executor
    to emulate ha component calls
"""
import logging
import pytest
import asyncio
from collections.abc import (
    Callable,
)

from sonnen_api_v2 import Batterie
from sonnenbatterie import sonnenbatterie

from . mock_sonnenbatterie_v2_charging import  __mock_configurations, __mock_battery, __mock_powermeter
from . mock_sonnenbatterie_v2_discharging import __mock_status_discharging, __mock_latest_discharging, __mock_inverter_discharging

LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@pytest.fixture(name="battery_discharging")
async def fixture_battery_discharging(mocker) -> Batterie:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data battery_discharging_asyncio test.')

    # Can't mock a coroutine!
    mocker.patch.object(Batterie, "fetch_status", __mock_status_discharging)
    mocker.patch.object(Batterie, "fetch_latest_details", __mock_latest_discharging)
    mocker.patch.object(Batterie, "fetch_configurations", __mock_configurations)
    mocker.patch.object(Batterie, "fetch_battery_status", __mock_battery)
    mocker.patch.object(Batterie, "fetch_powermeter", __mock_powermeter)
    mocker.patch.object(Batterie, "fetch_inverter", __mock_inverter_discharging)

    def async_add_executor_job[*_Ts, _T](
        target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        loop = asyncio.get_running_loop()
        task = loop.run_in_executor(None, target, *args)
        return task

    def _setup_batterie(_username, _token, _host):
        """Coroutine to sync instantiation"""
        return sonnenbatterie(_username, _token, _host)

    battery_discharging:sonnenbatterie = await async_add_executor_job(
        _setup_batterie, 'fakeUsername', 'fakeToken', 'fakeHost'
    )

    def _sync_update(battery_discharging: sonnenbatterie) -> bool:
        """Coroutine to sync fetch"""
        return battery_discharging.get_update()

    success = await async_add_executor_job(
        _sync_update, battery_discharging
    )
    assert success is not False

    return battery_discharging
