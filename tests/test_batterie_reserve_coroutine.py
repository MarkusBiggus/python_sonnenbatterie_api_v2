"""pytest tests/test_batterie_reserve_coroutine.py -s -v -x
3. Sync update called from coroutine passed to asyncio.run_in_executor
"""
#import datetime
import os
import sys
import logging
import pytest
#import pytest_asyncio
#from pytest_mock import mocker
import asyncio
from collections.abc import (
    Callable,
)

#from freezegun import freeze_time
#from sonnen_api_v2 import Batterie
from sonnenbatterie import sonnenbatterie

from .battery_discharging_reserve_coroutine import fixture_battery_discharging_reserve

LOGGER_NAME = None # "sonnenapiv2" #

logging.getLogger("asyncio").setLevel(logging.WARNING)

if LOGGER_NAME is not None:
    filename=f'tests/logs/{LOGGER_NAME}.log'
    logging.basicConfig(filename=filename, level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(LOGGER_NAME)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs debug messages
    fh = logging.FileHandler(filename=filename, mode='a')
    fh.setLevel(logging.DEBUG)
    # console handler display logs messages to console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info ('Coroutine mock data tests')


@pytest.mark.asyncio
@pytest.mark.usefixtures("battery_discharging_reserve")
async def test_coroutine_methods(battery_discharging_reserve: sonnenbatterie) -> None:
    """Batterie coroutines using mock data"""

    def async_add_executor_job[*_Ts, _T](
        target: Callable[[*_Ts], _T], *args: *_Ts
        ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        loop = asyncio.get_running_loop()
        task = loop.run_in_executor(None, target, *args)
        return task

    def _test_get_status():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_status()

    def _test_get_systemdata():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_systemdata()

    def _test_get_latest_data():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_latest_data()

    def _test_get_configurations():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_configurations()

    def _test_get_battery():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_battery()

    def _test_get_batterysystem():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_batterysystem()

    def _test_get_powermeter():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_powermeter()

    def _test_get_inverter():
        """Coroutine to sync fetch"""
        return battery_discharging_reserve.get_inverter()


    # sync wrapped methods used by ha component called by syncio.run_in_executor
    status_data = await async_add_executor_job(
        target=_test_get_status
    )
    latest_data = await async_add_executor_job(
        target=_test_get_latest_data
    )
    #print(f'status: {status_data}')
    assert status_data.get('Timestamp') == latest_data.get('Timestamp')
    assert status_data.get('GridFeedIn_W') == latest_data.get('GridFeedIn_W')
    assert status_data.get('Consumption_W') == latest_data.get('Consumption_W')
    assert status_data.get('Production_W') == latest_data.get('Production_W')
    assert status_data.get('Pac_total_W') == latest_data.get('Pac_total_W')

    assert status_data.get('Timestamp') == '2023-11-20 17:00:59'
    assert status_data.get('GridFeedIn_W') == 0
    assert status_data.get('Consumption_W') == 1541
    assert status_data.get('Production_W') == 103
    assert status_data.get('Pac_total_W') == 1438

    assert latest_data.get('Timestamp') == '2023-11-20 17:00:59'
    assert latest_data.get('GridFeedIn_W') == 0
    assert latest_data.get('Consumption_W') == 1541
    assert latest_data.get('Production_W') == 103
    assert latest_data.get('Pac_total_W') == 1438

    powermeter = await async_add_executor_job(
        target=_test_get_powermeter
    )
    assert powermeter[0]['direction'] == 'production'
    assert powermeter[0]['kwh_imported'] == 3969.800048828125
    assert powermeter[1]['direction'] == 'consumption'
    assert powermeter[1]['kwh_imported'] == 816.5

    battery_status = await async_add_executor_job(
        target=_test_get_battery
    )
    assert battery_status.get('cyclecount') == 30
    assert battery_status.get('remainingcapacity') == 36.36
    assert battery_status.get('nominalmoduledcvoltage') == 102.4
    assert battery_status.get('usableremainingcapacity') == 22.22

    assert battery_status.get('total_installed_capacity') == 20000
    assert battery_status.get('remaining_capacity') == 3723.264
    assert battery_status.get('remaining_capacity_usable') == 2275.328
    assert battery_status.get('backup_buffer_usable') == 2688

    assert battery_status.get('current_state') == 'discharging'

    system_data = await async_add_executor_job(
        target=_test_get_systemdata
    )
    assert system_data.get('software_version') == '1.14.5'

    battery_system = await async_add_executor_job(
        target=_test_get_batterysystem
    )
    print(f'battery: {battery_system['battery_system']}')
    assert battery_system['battery_system']['system']['depthofdischargelimit'] == 93
    assert battery_system.get('modules') == 4

    inverter_data = await async_add_executor_job(
        target=_test_get_inverter
    )
    assert inverter_data.get('pac_total') == status_data.get('Pac_total_W')
    assert inverter_data.get('pac_total') == 1438
    assert inverter_data.get('uac') == 233.55

    configurations = await async_add_executor_job(
        target=_test_get_configurations
    )
    assert configurations.get('DE_Software') == system_data.get('software_version')
    assert configurations.get('DE_Software') == '1.14.5'
    assert configurations.get('EM_USOC') == 20
    assert configurations.get('DepthOfDischargeLimit') == 93

    # every other emulated get methods
    request_connect_timeouts = battery_discharging_reserve.get_request_connect_timeouts()
    #print(f'connect_timeouts: {request_connect_timeouts}')
    assert request_connect_timeouts == (20,20)
    request_connect_timeouts = battery_discharging_reserve.set_request_connect_timeouts((15,25))
    assert request_connect_timeouts == (15,25)

    operating_mode =  battery_discharging_reserve.configuration_em_operatingmode
    operating_mode_name =  battery_discharging_reserve.configuration_em_operatingmode_name
    battery_reserve =  battery_discharging_reserve.configuration_em_usoc
    #print(f'operating_mode: {operating_mode}  name: {operating_mode_name}  battery_reserve:{battery_reserve}%')
    assert battery_reserve == 20
    assert operating_mode == 2
    assert operating_mode_name == 'Automatic - Self Consumption'

    from .check_results import check_reserve_results

    check_reserve_results(battery_discharging_reserve)
