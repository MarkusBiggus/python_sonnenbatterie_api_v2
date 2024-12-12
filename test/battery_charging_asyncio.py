import os
import logging
import pytest
import asyncio
from collections.abc import (
    Callable,
)
from asyncmock import AsyncMock

from sonnen_api_v2 import Batterie
from sonnenbatterie import sonnenbatterie

from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter


LOGGER_NAME = "sonnenapiv2"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@pytest.fixture(name="battery_charging")
async def fixture_battery_charging(mocker) -> sonnenbatterie:
    if LOGGER_NAME is not None:
        logging.basicConfig(filename=(f'/tests/logs/{LOGGER_NAME}.log'), level=logging.DEBUG)
        logger = logging.getLogger(LOGGER_NAME)
        logger.info('Sonnen mock data battery_charging_asyncio test.')

    mocker.patch.object(Batterie, "async_fetch_status", AsyncMock(return_value=__mock_status_charging()))
    mocker.patch.object(Batterie, "async_fetch_latest_details", AsyncMock(return_value=__mock_latest_charging()))
    mocker.patch.object(Batterie, "async_fetch_configurations", AsyncMock(return_value=__mock_configurations()))
    mocker.patch.object(Batterie, "fetch_configurations", __mock_configurations)
    mocker.patch.object(Batterie, "async_fetch_battery_status", AsyncMock(return_value=__mock_battery()))
    mocker.patch.object(Batterie, "async_fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))
    mocker.patch.object(Batterie, "async_fetch_inverter", AsyncMock(return_value=__mock_inverter()))

    def async_add_executor_job[*_Ts, _T](
        self, target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        self.loop = asyncio.get_running_loop()
        task = self.loop.run_in_executor(None, target, *args)
    #    print (f'task type: {type(task)}')
        return task

    def _setup_batterie(_username, _token, _host):
        """Coroutine to sync instantiation"""
        return sonnenbatterie(_username, _token, _host)

    battery_charging:sonnenbatterie = await async_add_executor_job(mocker,
        _setup_batterie, 'fakeUsername', 'fakeToken', 'fakeHost'
    )

    return battery_charging
