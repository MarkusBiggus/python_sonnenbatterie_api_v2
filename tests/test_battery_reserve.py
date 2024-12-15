"""python -m unittest test.test_battery_reserve """

import os, sys
import unittest
import json

from sonnenbatterie.const import *
from sonnenbatterie import sonnenbatterie

from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST','X')
API_READ_TOKEN = os.getenv('API_READ_TOKEN','X')
API_WRITE_TOKEN = os.getenv('API_WRITE_TOKEN','X')

LOGGER_NAME = None # "battery_reserve" #


if BATTERIE_HOST == 'X' or (API_WRITE_TOKEN == 'X'and API_READ_TOKEN == 'X'):
    print(f'host: {BATTERIE_HOST} WRITE: {API_WRITE_TOKEN} READ: {API_READ_TOKEN}')
    raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN or API_WRITE_TOKEN in .env See env.example')

logging.getLogger("battery_reserve").setLevel(logging.WARNING)

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
    logger.info ('Live batterie reserve tests')


def test_battery_reserve():
    _battery = sonnenbatterie('', API_WRITE_TOKEN if API_WRITE_TOKEN != 'X' else API_READ_TOKEN, BATTERIE_HOST)
    configurations = _battery.get_configurations()
    assert configurations.get('DE_Software') == '1.15.6'

    battery_reserve = _battery.get_battery_reserve()
    current_charge = _battery.get_current_charge_level()
    print(f'battery_reserve: {battery_reserve}%   current_charge: {current_charge:,}%')

    OperatingMode = _battery.get_configuration(SONNEN_CONFIGURATION_OPERATING_MODE)
    TOU = _battery.get_configuration(SONNEN_CONFIGURATION_TOU_SCHEDULE)
    print (f'Operating Mode: {OperatingMode}  TOU_SCHEDULE: {TOU}')
    connect_timeout = _battery.get_request_connect_timeout()
    request_timeout = _battery.get_request_read_timeout()
    print (f'connect_timeout: {connect_timeout}s  request_timeout: {request_timeout}s')
    assert (60, 60) == (connect_timeout, request_timeout)
    request_timeouts = _battery.set_request_connect_timeout(15)
    assert request_timeouts == (15,60)
    request_timeouts = _battery.set_request_read_timeout(25)
    assert request_timeouts == (15,25)

    battery_status = _battery.get_battery()
#    print('battery status: ' + json.dumps(battery_status, indent=2))
    RSOC = battery_status.get("relativestateofcharge")
    URC = battery_status.get("usableremainingcapacity")
    RC = battery_status.get("remainingcapacity")
    FC = battery_status.get("fullchargecapacity")
    DCV = battery_status.get("nominalmoduledcvoltage")
    URCWH = URC * DCV
    print (f'relativestateofcharge: {RSOC:.1f}%')
    print (f'usableremainingcapacity: {URC:.3f}Ah  remainingcapacity: {RC:.2f}Ah  fullchargecapacity: {FC:.3f}Ah')
    print (f'nominalmoduledcvoltage: {DCV:.2f}V  usableremainingcapacity: {URCWH:,.1f}Wh')

    system_status = _battery.get_status()
#    print('system status: ' + json.dumps(system_status, indent=2))
    CW = system_status.get("Consumption_W")
    PW = system_status.get("Production_W")
    GFIW = system_status.get("GridFeedIn_W")
    PAC = system_status.get("Pac_total_W")
    charging = system_status.get("BatteryCharging") #== 'true'
    discharging = system_status.get("BatteryDischarging") #== 'true'
    if discharging:
        print (f'Consumption: {CW}W  PAC: {PAC}W  Battery Discharging {discharging}')
    elif charging:
        print (f'Consumption: {CW}W  PAC: {PAC}W  Production: {PW}W  GridFeedIn: {GFIW}W  Battery Charging {charging}')
    else:
        if GFIW > 0:
            print (f'Consumption: {CW}W  PAC: {PAC}W  Production: {PW}W  GridFeedIn: {GFIW}W  Battery on standby')
        else:
            print (f'Consumption: {CW}W  PAC: {PAC}W  GridUse: {abs(GFIW)}W  Battery at reserve')

    powermeter = _battery.get_powermeter()
#    print('powermeter: ' + json.dumps(powermeter, indent=2))
    print (f'Power Meter: {powermeter[0]["direction"]} {powermeter[0]["w_total"]:,.2f}W  {powermeter[1]["direction"]} {powermeter[1]["w_total"]:,.2f}W')

    inverter = _battery.get_inverter()
#    print('inverter: ' + json.dumps(inverter, indent=2))
    PAC = inverter.get("pac_total")
    print (f'inverter PAC: {PAC:.2f}W ')

    latest_data = _battery.get_latest_data()
#    print('latest_data: ' + json.dumps(latest_data, indent=2))
    CW = latest_data.get("Consumption_W")
    PAC = latest_data.get("Pac_total_W")
    RSOC = latest_data.get("RSOC")
    print (f'latest Consumption: {CW}W  PAC: {PAC}W  RSOC: {RSOC}%')
