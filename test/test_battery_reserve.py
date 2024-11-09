"""pytest tests/test_battey_reserve.py -s -x -v """

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

class TestBatterie(unittest.TestCase):

    if BATTERIE_HOST == 'X' or (API_WRITE_TOKEN == 'X'and API_READ_TOKEN == 'X'):
        print(f'host: {BATTERIE_HOST} WRITE: {API_WRITE_TOKEN} READ: {API_READ_TOKEN}')
        raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN or API_WRITE_TOKEN in .env See env.example')

    def setUp(self) -> None:
        self._battery = sonnenbatterie('', API_WRITE_TOKEN if API_WRITE_TOKEN != 'X' else API_READ_TOKEN, BATTERIE_HOST)
        success = self._battery.get_configurations()
        if not success:
            self.skipTest("Failed to get battery data.")

    def test_reserve(self):
        battery_reserve = self._battery.get_battery_reserve()
        current_charge = self._battery.get_current_charge_level()
        print(f'battery_reserve: {battery_reserve}%   current_charge: {current_charge:,}%')

    def test_config(self):
        OperatingMode = self._battery.get_configuration(SONNEN_CONFIGURATION_OPERATING_MODE)
        TOU = self._battery.get_configuration(SONNEN_CONFIGURATION_TOU_SCHEDULE)
        print (f'Operating Mode: {OperatingMode}  TOU_SCHEDULE: {TOU}')
        connect_timeout = self._battery.get_request_connect_timeout()
        request_timeout = self._battery.get_request_read_timeout()
        print (f'connect_timeout: {connect_timeout}s  request_timeout: {request_timeout}s')
        self.assertEqual( (60, 60), (connect_timeout, request_timeout) )

    def test_battery(self):
        battery_status = self._battery.get_battery()
    #    print('battery status: ' + json.dumps(battery_status, indent=2))
        RSOC = battery_status.get("relativestateofcharge")
        URC = battery_status.get("usableremainingcapacity")
        RC = battery_status.get("remainingcapacity")
        FC = battery_status.get("fullchargecapacity")
        DCV = battery_status.get("systemdcvoltage")
        URCWH = URC * DCV
        print (f'relativestateofcharge: {RSOC:.1f}%')
        print (f'usableremainingcapacity: {URC:.3f}Ah  remainingcapacity: {RC:.2f}Ah  fullchargecapacity: {FC:.3f}Ah')
        print (f'systemdcvoltage: {DCV:.2f}V  usableremainingcapacity: {URCWH:,.1f}Wh')

    def test_status(self):
        system_status = self._battery.get_status()
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

    def test_powermeter(self):
        powermeter = self._battery.get_powermeter()
    #    print('powermeter: ' + json.dumps(powermeter, indent=2))
        print (f'Power Meter: {powermeter[0]["direction"]} {powermeter[0]["w_total"]:,.2f}W  {powermeter[1]["direction"]} {powermeter[1]["w_total"]:,.2f}W')

    def test_inverter(self):
        inverter = self._battery.get_inverter()
    #    print('inverter: ' + json.dumps(inverter, indent=2))
        PAC = inverter.get("pac_total")
        print (f'inverter PAC: {PAC:.2f}W ')

    def test_latest_data(self):
        latest_data = self._battery.get_latest_data()
    #    print('latest_data: ' + json.dumps(latest_data, indent=2))
        CW = latest_data.get("Consumption_W")
        PAC = latest_data.get("Pac_total_W")
        RSOC = latest_data.get("RSOC")
        print (f'latest Consumption: {CW}W  PAC: {PAC}W  RSOC: {RSOC}%')
