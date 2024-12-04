"""pytest test/test_battery_mock.py -s -v -x
"""
#import datetime
import os
import sys

import logging
import pytest

from asyncmock import AsyncMock
#import json
from dotenv import load_dotenv

from sonnen_api_v2.sonnen import Sonnen as Batterie


from . mock_sonnenbatterie_v2_charging import __mock_status_charging, __mock_latest_charging, __mock_configurations, __mock_battery, __mock_powermeter, __mock_inverter

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST','X')
BATTERIE_PORT = '80'
API_READ_TOKEN = os.getenv('API_READ_TOKEN')
# BATTERIE_1_HOST = os.getenv('BATTERIE_1_HOST','X')
# API_READ_TOKEN_1 = os.getenv('API_READ_TOKEN_1')
# BATTERIE_2_HOST = os.getenv('BATTERIE_2_HOST')
# API_READ_TOKEN_2 = os.getenv('API_READ_TOKEN_2')

LOGGER_NAME = None # "sonnenapiv2" #


if BATTERIE_HOST == 'X':
    raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN in .env See env.example')

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
async def test_get_batterie_charging(mocker):

    """Batterie charging using mock data"""
    mocker.patch.object(Batterie, "fetch_configurations", AsyncMock(return_value=__mock_configurations()))
    mocker.patch.object(Batterie, "fetch_status", AsyncMock(return_value=__mock_status_charging()))
    mocker.patch.object(Batterie, "fetch_latest_details", AsyncMock(return_value=__mock_latest_charging()))
    mocker.patch.object(Batterie, "fetch_powermeter", AsyncMock(return_value=__mock_powermeter()))
    mocker.patch.object(Batterie, "fetch_battery_status", AsyncMock(return_value=__mock_battery()))
    mocker.patch.object(Batterie, "fetch_inverter_data", AsyncMock(return_value=__mock_inverter()))

    _battery = Batterie(API_READ_TOKEN, BATTERIE_HOST, BATTERIE_PORT, LOGGER_NAME)  # Batterie online

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
