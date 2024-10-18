import os
import unittest
#import sys
#import json
#import logging
from sonnen_api_v2 import Sonnen
#from sonnen_api_v2 import *
from dotenv import load_dotenv

load_dotenv()

BATTERIE_HOST = os.getenv('BATTERIE_HOST','X')
API_READ_TOKEN = os.getenv('API_READ_TOKEN')
API_WRITE_TOKEN = os.getenv('API_WRITE_TOKEN','X')
# SonnenBatterie config parameters to check against
BACKUP_BUFFER_USOC = int(os.getenv('BACKUP_BUFFER_USOC'))
OPERATING_MODE = int(os.getenv('OPERATING_MODE'))
LOGGER_NAME = "sonnenapiv2"

class TestBatterie(unittest.TestCase):

    if BATTERIE_HOST == 'X' or (API_WRITE_TOKEN == 'X'and API_READ_TOKEN == 'X'):
        raise ValueError('Set BATTERIE_HOST & API_READ_TOKEN or API_WRITE_TOKEN in .env See env.example')

    print ('Live Battery Online!')

    def setUp(self) -> None:
#        os.makedirs(os.path.dirname('logs/'+LOGGER_NAME+'.log'), exist_ok=True)
#        self.logger = logging.getLogger(LOGGER_NAME)
#        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs debug messages
#        fh = logging.FileHandler(filename='logs/'+LOGGER_NAME+'.log', mode='a')
#        fh.setLevel(logging.DEBUG)
        # console handler display logs messages to console
#        ch = logging.StreamHandler(sys.stdout)
#        ch.setLevel(logging.DEBUG)
#        self.logger.addHandler(fh)
#        self.logger.addHandler(ch)
#        self.logger.info('Sonnen Live Batterie Test suite started.')

        self.battery_live = Sonnen(API_READ_TOKEN, BATTERIE_HOST, LOGGER_NAME)  # Batterie online

        self.battery_live.set_request_connect_timeouts( (20, 10) )
        success = self.battery_live.update()
        self.assertTrue(success)

    def test_configuration_de_software(self):
#        self.logger.info('test_configuration_de_software')
        version = self.battery_live.configuration_de_software
        cycles = self.battery_live.battery_cycle_count
        print(f'Software Version: {version}   Battery Cycles: {cycles:,}')
        self.assertEqual(True, True)

    def test_configuration_em_usoc(self):
        usoc = self.battery_live.configuration_em_usoc
        self.assertEqual(usoc, BACKUP_BUFFER_USOC) # config BackupBuffer value

    def test_system_status(self):
        state = self.battery_live.state_core_control_module
        print (f'Core Control State: {state}')
        status = self.battery_live.system_status
        print (f'System Status: {status}')
        status_timestamp = self.battery_live.system_status_timestamp
        print (f'Status time: {status_timestamp.strftime("%d-%b-%Y %H:%M:%S")}')
        validation_timestamp = self.battery_live.validation_timestamp
        print (f'Validation time: {validation_timestamp.strftime("%d-%b-%Y %H:%M:%S")}')
        self.assertEqual(state, 'ongrid')
        self.assertEqual(status, 'OnGrid')
