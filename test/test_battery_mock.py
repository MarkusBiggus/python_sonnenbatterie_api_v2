"""pytest test/test_battery_mock.py -s -v -x
"""
#import datetime
import os
import sys

import logging
import pytest

from asyncmock import AsyncMock
#import json

#from sonnen_api_v2.sonnen import Sonnen as Batterie
from sonnen_api_v2 import Batterie
from sonnenbatterie import sonnenbatterie


from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter


LOGGER_NAME = None # "sonnenapiv2" #


logging.getLogger("mock_batterie").setLevel(logging.WARNING)

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
    logger.info ('Asyncio mock batterie tests')


@pytest.mark.asyncio
async def test_sonnen_package(mocker):
    """sonnen_api_v2 package: Batterie charging using mock data"""
    mocker.patch.object(Batterie, "fetch_configurations", AsyncMock(return_value=__mock_configurations()))
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=__mock_status_charging()))
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=__mock_latest_charging()))
    mocker.patch.object(Batterie, "fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))
    mocker.patch.object(Batterie, "fetch_battery_status", AsyncMock(return_value=__mock_battery()))
    mocker.patch.object(Batterie, "fetch_inverter_data", AsyncMock(return_value=__mock_inverter()))

    _battery = Batterie('fakeToken', 'fakeHost', '80')

    await _battery.async_update()
    version = _battery.configuration_de_software # mock_configurations
    status = _battery.system_status # latest_charging
    backup_buffer = _battery.status_backup_buffer # status_charging
    kwh_consumed = _battery.kwh_consumed # mock_powermeter
    cycles = _battery.battery_cycle_count # mock_battery
    PAC_total = _battery.inverter_pac_total # mock_inverter

    print(f'\n\rStatus: {status}  Software Version: {version}   Battery Cycles: {cycles:,}')
    print(f'PAC: {PAC_total:,.2f}W  Consumed: {kwh_consumed:,.2f}  Backup Buffer: {backup_buffer}%')
    assert status == 'OnGrid'
    assert cycles == 30
    assert version == '1.14.5'
    assert PAC_total == -1394.33
    assert backup_buffer == 20
    assert kwh_consumed == 816.5
    total_installed_capacity = _battery.installed_capacity
    batt_reserve_percent = _battery.status_backup_buffer
    total_capacity_raw = _battery.battery_full_charge_capacity_wh
    reserved_capacity = int(
            total_installed_capacity * batt_reserve_percent / 100.0
        )
    remaining_capacity = (
            int(total_capacity_raw * _battery.battery_rsoc) / 100.0
        )
    remaining_capacity_usable = max(
            0, int(remaining_capacity - reserved_capacity))
    print(f'remaining_capacity (raw): {remaining_capacity:,}Wh  remaining_usable (raw): {remaining_capacity_usable:,}Wh')
    print(f'full_charge_capacity (raw): {total_capacity_raw:,}Wh')


#@pytest.mark.asyncio
#async def test_batterie_emulator(mocker):
def test_batterie_emulator(mocker):
    """sonnenbatterie_api_v2 package: Batterie charging using mock data"""
    mocker.patch.object(sonnenbatterie, "check_status", AsyncMock(return_value=__mock_status_charging()))
    _battery = sonnenbatterie("", 'fakeToken', 'fakeHost')

    mocker.patch.object(_battery.batterie, "fetch_configurations", AsyncMock(return_value=__mock_configurations()))
    mocker.patch.object(_battery.batterie, "fetch_latest_details", AsyncMock(return_value=__mock_latest_charging()))
    mocker.patch.object(_battery.batterie, "fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))
    mocker.patch.object(_battery.batterie, "fetch_battery_status", AsyncMock(return_value=__mock_battery()))
    mocker.patch.object(_battery.batterie, "fetch_inverter_data", AsyncMock(return_value=__mock_inverter()))

    #same package tests above via emulator
    _battery.batterie.update() # get mocked response
#    await _battery.batterie.async_update()
    version = _battery.batterie.configuration_de_software # mock_configurations
    status = _battery.batterie.system_status # latest_charging
    backup_buffer = _battery.batterie.status_backup_buffer # status_charging
    kwh_consumed = _battery.batterie.kwh_consumed # mock_powermeter
    cycles = _battery.batterie.battery_cycle_count # mock_battery
    PAC_total = _battery.batterie.inverter_pac_total # mock_inverter

    print(f'\n\rStatus: {status}  Software Version: {version}   Battery Cycles: {cycles:,}')
    print(f'PAC: {PAC_total:,.2f}W  Consumed: {kwh_consumed:,.2f}  Backup Buffer: {backup_buffer}%')
    assert status == 'OnGrid'
    assert cycles == 30
    assert version == '1.14.5'
    assert PAC_total == -1394.33
    assert backup_buffer == 20
    assert kwh_consumed == 816.5

    total_installed_capacity = _battery.batterie.installed_capacity
    batt_reserve_percent = _battery.batterie.status_backup_buffer
    total_capacity_raw = _battery.batterie.battery_full_charge_capacity_wh
    reserved_capacity = int(
            total_installed_capacity * batt_reserve_percent / 100.0
        )
    remaining_capacity = (
            int(total_capacity_raw * _battery.battery_rsoc) / 100.0
        )
    remaining_capacity_usable = max(
            0, int(remaining_capacity - reserved_capacity))
    print(f'remaining_capacity (raw): {remaining_capacity:,}Wh  remaining_usable (raw): {remaining_capacity_usable:,}Wh')
    print(f'full_charge_capacity (raw): {total_capacity_raw:,}Wh')

    #emulated methods
    latestData = {}

    latestData["battery_system"] = _battery.get_batterysystem()
    #print(f'battery_system type: {type(latestData["battery_system"])}')
    latestData["status"] = _battery.get_status()
    latestData["battery_info"] = _battery.get_battery()
    batt_module_capacity = int(
        latestData["battery_system"]["battery_system"]["system"][
            "storage_capacity_per_module"
        ]
    )
    dod = int(latestData["battery_system"]["battery_system"]["system"]['depthofdischargelimit'])
    batt_reserve_percent = 100 - dod
    batt_module_count = int(latestData["battery_system"]["modules"])
    total_installed_capacity = int(batt_module_count * batt_module_capacity)
    print(f'module_capacity: {batt_module_capacity:,}Wh  module_count: {batt_module_count}  Installed Capacity: {total_installed_capacity:,}Wh')
    total_capacity_raw = _battery.batterie.battery_full_charge_capacity_wh
    reserved_capacity = int(
            total_installed_capacity * batt_reserve_percent / 100.0
        )
    remaining_capacity = (
            int(total_capacity_raw * _battery.batterie.battery_rsoc) / 100.0
        )
    remaining_capacity_usable = max(
            0, int(remaining_capacity - reserved_capacity))
    print(f'remaining_capacity (raw): {remaining_capacity:,}Wh  remaining_usable (raw): {remaining_capacity_usable:,}Wh')
    print(f'full_charge_capacity (raw): {total_capacity_raw:,}Wh')
