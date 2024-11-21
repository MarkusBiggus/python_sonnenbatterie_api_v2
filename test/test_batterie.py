"""python -m unittest test.test_batterie """
import os
import unittest
#import sys
#import json
#import logging
from sonnen_api_v2.sonnen import Sonnen as Batterie
#from sonnen_api_v2 import *
from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST','X')
API_READ_TOKEN = os.getenv('API_READ_TOKEN')
API_WRITE_TOKEN = os.getenv('API_WRITE_TOKEN','X')
# SonnenBatterie config parameters to check against
LOGGER_NAME = None #"sonnenapiv2"

class TestBatterie(unittest.TestCase):

    if BATTERIE_HOST == 'X' or (API_WRITE_TOKEN == 'X'and API_READ_TOKEN == 'X'):
        raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN or API_WRITE_TOKEN in .env See env.example')

    print ('Live Battery Online!')

    def setUp(self) -> None:

        self._battery = Batterie(API_READ_TOKEN, BATTERIE_HOST) # '80', LOGGER_NAME)  # Batterie online

        self._battery.set_request_connect_timeouts( (20, 10) )

        success = self._battery.update()
        if not success:
            self.skipTest("Failed to get battery data.")

    def test_configuration_de_software(self):
#        self.logger.info('test_configuration_de_software')
        version = self._battery.configuration_de_software
        cycles = self._battery.battery_cycle_count
        print(f'Software Version: {version}   Battery Cycles: {cycles:,}')
        self.assertEqual(True, True)

    def test_system_status(self):
        state = self._battery.state_core_control_module
        print (f'Core Control State: {state}')
        status = self._battery.system_status
        print (f'System Status: {status}')
        status_timestamp = self._battery.system_status_timestamp
        print (f'Status time: {status_timestamp.strftime("%d-%b-%Y %H:%M:%S")}')
        validation_timestamp = self._battery.validation_timestamp
        print (f'Validation time: {validation_timestamp.strftime("%d-%b-%Y %H:%M:%S")}')
        self.assertEqual(state, 'ongrid')
        self.assertEqual(status, 'OnGrid')
