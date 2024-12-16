#import os
#from dotenv import load_dotenv
#import hashlib
import asyncio
from collections.abc import (
    Callable,
)
from typing import (
    Union,
    Dict,
)
#import requests
import json
from .const import *
from .timeofuse import timeofuseschedule
from sonnen_api_v2 import Batterie, BatterieError

# indexes for _batteryRequestTimeouts
TIMEOUT_CONNECT=0
TIMEOUT_REQUEST=1

#load_dotenv()

class sonnenbatterie:
    def __init__(self, username, token, ipaddress) -> None:
        """Expect to be in a running asyncio loop called by asyncio.loop.run_in_executor
            Condition of HA custom_component.coordinator _async_update_data()
            that instantiates this class
        """
#        self.username=username
        self.token=token
        self.ipaddress=ipaddress
        self.baseurl='http://'+self.ipaddress+'/api/'
        self.setpoint='v2/setpoint/'
        self._batteryLoginTimeout = DEFAULT_BATTERY_LOGIN_TIMEOUT
#        self._batteryConnectTimeout = DEFAULT_CONNECT_TO_BATTERY_TIMEOUT
#        self._batteryReadTimeout = DEFAULT_READ_FROM_BATTERY_TIMEOUT
#        self._batteryRequestTimeouts = (self._batteryConnectTimeout, self._batteryReadTimeout)
        self._batteryRequestTimeouts = (DEFAULT_CONNECT_TO_BATTERY_TIMEOUT, DEFAULT_READ_FROM_BATTERY_TIMEOUT)
        self.configurations = None
        self.batterie = Batterie(self.token, self.ipaddress)
        # Expect to be in a running loop from ha

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        try:
            self.configurations = self.batterie.sync_get_configurations() # cache configurations in Batterie
        except BatterieError as error:
            LOGGER.error(f'Error connecting to sonnenbatterie! {error}')
            raise BatterieError(f'Error connecting to sonnenbatterie! {error}')

        if self.configurations is None:
            LOGGER.error('Unable to fetch config from sonnenbatterie!')
            raise BatterieError('Unable to fetch config from sonnenbatterie!')

        self.batterie.set_request_connect_timeouts(self._batteryRequestTimeouts)
        self.set_login_timeout()
        self._battery_serial_number = 'unknown' #os.getenv("BATTERIE_SN", "unknown")
        self._battery_model = 'unknown' #os.getenv("BATTERIE_MODEL", "unknown")
#        self._login()

    def _login(self):
        """not required for V2 API"""
#        password_sha512 = hashlib.sha512(self.password.encode('utf-8')).hexdigest()
#        req_challenge=requests.get(self.baseurl+'challenge', timeout=self._batteryLoginTimeout)
#        req_challenge.raise_for_status()
#        challenge=req_challenge.json()
#        response=hashlib.pbkdf2_hmac('sha512',password_sha512.encode('utf-8'),challenge.encode('utf-8'),7500,64).hex()

        #print(password_sha512)
        #print(challenge)
        #print(response)
#        getsession=requests.post(self.baseurl+'session',{"user":self.username,"challenge":challenge,"response":response}, timeout=self._batteryLoginTimeout)
#        getsession.raise_for_status()
        #print(getsession.text)
#        token=getsession.json()['authentication_token']
        #print(token)
#        self.token=token

    def set_login_timeout(self, timeout:int = 120):
        # not used by wrapper
        self._batteryLoginTimeout = timeout
        return self._batteryLoginTimeout

    def get_login_timeout(self) -> int:
        return self._batteryLoginTimeout

    def set_request_connect_timeout(self, timeout:int = DEFAULT_CONNECT_TO_BATTERY_TIMEOUT) -> tuple[int,int]:
        self._batteryRequestTimeouts = self.batterie.set_request_connect_timeouts ((timeout, self._batteryRequestTimeouts[TIMEOUT_REQUEST]))
        return self._batteryRequestTimeouts[TIMEOUT_CONNECT]

    def get_request_connect_timeout(self) -> int:
        return self._batteryRequestTimeouts[TIMEOUT_CONNECT]

    def set_request_read_timeout(self, timeout:int = DEFAULT_READ_FROM_BATTERY_TIMEOUT):
        self._batteryRequestTimeouts = self.batterie.set_request_connect_timeouts ((self._batteryRequestTimeouts[TIMEOUT_CONNECT], timeout))
        return self._batteryRequestTimeouts[TIMEOUT_REQUEST]

    def get_request_read_timeout(self) -> int:
        return self._batteryRequestTimeouts[TIMEOUT_REQUEST]

    # def _get(self,what,isretry=False):
    #     # This is a synchronous call, you may need to wrap it in a thread or something for asynchronous operation
    #     url = self.baseurl+what
    #     response=requests.get(url,
    #         headers={'Auth-Token': self.token}, timeout=self._batteryRequestTimeouts
    #     )
    #     if not isretry and response.status_code == 401:
    #         self._login()
    #         return self._get(what,True)
    #     if response.status_code != 200:
    #         response.raise_for_status()

    #     return response.json()

    # def _put(self, what, payload, isretry=False):
    #     # This is a synchronous call, you may need to wrap it in a thread or something for asynchronous operation
    #     url = self.baseurl+what
    #     response=requests.put(url,
    #         headers={'Auth-Token': self.token,'Content-Type': 'application/json'} , json=payload, timeout=self._batteryRequestTimeouts
    #     )
    #     if not isretry and response.status_code == 401:
    #         self._login()
    #         return self._put(what, payload,True)
    #     if response.status_code != 200:
    #         response.raise_for_status()
    #     return response.json()

    # def _post(self, what, isretry=False):
    #     # This is a synchronous call, you may need to wrap it in a thread or something for asynchronous operation
    #     url = self.baseurl+what
    #     print("Posting "+url)
    #     response=requests.post(url,
    #         headers={'Auth-Token': self.token,'Content-Type': 'application/json'}, timeout=self._batteryRequestTimeouts
    #     )
    #     if not isretry and response.status_code == 401:
    #         self._login()
    #         return self._post(what, True)
    #     if response.status_code != 200:
    #         response.raise_for_status()
    #     return response

    # def async_add_executor_job[*_Ts, _T](
    #     self, target: Callable[[*_Ts], _T], *args: *_Ts
    #     ) -> asyncio.Future[_T]:
    #     """Add an executor job from within the event loop."""
    #     self.loop = asyncio.get_running_loop()
    #     task = self.loop.run_in_executor(None, target, *args)
    #     return task

    # these are special purpose endpoints, there is no associated data that I'm aware of
    # while I don't have details I belive this is probabaly only useful in manual more
    # and it's probabaly possible to extact the actuall flow rate in operation
    # looking at the status.state_battery_inout value
    # irritatingly there is no mechanism in the API to do a single set to you have to work out if
    # the direction of the flow and then call the appropriate API
    def set_manual_flowrate(self, direction, rate, isretry=False):
        path=self.setpoint+direction+"/"+str(rate)
        response = self._post(path)
        return (response.status_code == 201)

    def set_discharge(self, rate):
        return self.set_manual_flowrate(SONNEN_DISCHARGE_PATH, rate)

    def set_charge(self, rate):
        return self.set_manual_flowrate(SONNEN_CHARGE_PATH, rate)

    # testing - used by fixtures to setup mocked data
    def get_update(self) -> bool:
        """Calls underlying Batterie update to read &
            cache all mocked data when fixture is setup.
            Only intended to setup tests.
        """
        return self.batterie.sync_update()

    # more general purpose endpoints
    def set_configuration(self, name, value):
        # All configurations names and values are handled as strings, so force that
        payload = {str(name): str(value)}
        return self._put(SONNEN_API_PATH_CONFIGURATIONS, payload)

    def get_configurations(self) -> Dict:
        """Cache configurations - reused by many other methods
            Verifies connection to device when class is instantiated
        """
    #    return self._get(SONNEN_API_PATH_CONFIGURATIONS)
        if self.configurations is None:
            self.configurations = self.batterie.get_configurations()
        return self.configurations

    # async def async_get_configurations(self) -> Dict:
    #     """Cache configurations - reused by many other methods
    #     """
    # #    return self._get(SONNEN_API_PATH_CONFIGURATIONS)
    #     if self.configurations is None:
    #         self.configurations = await self.async_add_executor_job(
    #             self.batterie.sync_get_configurations
    #         )
    #     return self.configurations

    def get_configuration(self, name):
    #    return self._get(SONNEN_API_PATH_CONFIGURATIONS+"/"+name).get(name)
        if self.configurations is None:
            self.configurations = self.batterie.get_configurations()

        return self.configurations.get(name)

    def get_status(self) -> Dict:
    #    return self._get(SONNEN_API_PATH_STATUS)
        status_data = self.batterie.sync_get_status()
        return status_data

    def get_powermeter(self) -> Dict:
    #    return self._get(SONNEN_API_PATH_POWER_METER)
        return self.batterie.sync_get_powermeter()

    def get_inverter(self) -> Dict:
    #    return self._get(SONNEN_API_PATH_INVERTER)
        return self.batterie.sync_get_inverter()

    def get_systemdata(self) -> Dict:
        '''system_data not in V2 - fake it for required component attributes'''
    #    return self._get(SONNEN_API_PATH_SYSTEM_DATA)
        self.get_configurations()
        return self._systemdata()

    def _systemdata(self) -> Dict:
        '''system_data not in V2 - fake it for required component attributes'''
        systemdata = {'software_version': self.configurations.get("DE_Software"),
                      'ERP_ArticleName': self._battery_model,
                      'DE_Ticket_Number': self._battery_serial_number
                    }
        return systemdata

    def get_batterysystem(self) -> Dict:
        """battery_system not in V2 - fake it for required component attributes"""
        configurations = self.batterie.sync_get_configurations()
        return self._aug_batterysystem_data(configurations)

    def _aug_batterysystem_data(self, configurations_data: Dict) -> Dict:
        """Augment battery_system data for V1 compatibility"""
        systemdata = {'modules':
                        configurations_data.get('IC_BatteryModules'),
                        'battery_system':
                        {
                            'system':
                            {
                                'storage_capacity_per_module': configurations_data.get('CM_MarketingModuleCapacity'),
                                'depthofdischargelimit': configurations_data.get('DepthOfDischargeLimit'),
                            }
                        }
                    }
        return systemdata

    def get_battery(self) -> Dict:
        """Battery status for sonnenbatterie wrapper
            Fake V1 API data used by ha sonnenbatterie component
            Returns:
                json response
        """
        battery_status = self.batterie.sync_get_battery()
        self.get_configurations()
        self.get_status() #cache in self.batterie
        return self._battery_status(battery_status)

    def _battery_status(self, battery_status) -> Dict:
        measurements = {'battery_status': {'cyclecount': self.batterie.battery_cycle_count,
                                        'stateofhealth': int(battery_status.get('systemstatus'))
                                        }
                        }
        battery_status['measurements'] = measurements

        if self.configurations is None:
            battery_status['current_state'] = "unavailable"
            return battery_status

        """ current_state index of: ["standby", "charging", "discharging", "charged", "discharged"] """
        if self.batterie.status_battery_charging:
            battery_status['current_state'] = "charging"
        elif self.batterie.status_battery_discharging:
            battery_status['current_state'] = "discharging"
        elif self.batterie.battery_rsoc > 98:
            battery_status['current_state'] = "charged"
        elif self.batterie.battery_usable_remaining_capacity < 2:
            battery_status['current_state'] = "discharged"
        else:
            battery_status['current_state'] = "standby"

        return battery_status

    def get_latest_data(self) -> Dict:
    #    return self._get(SONNEN_API_PATH_LATEST_DATA)
        return self.batterie.sync_get_latest_data()

    # these have special handling in some form, for example converting a mode as a number into a string
    def get_current_charge_level(self) -> int:
    #    return self.get_latest_data().get(SONNEN_LATEST_DATA_CHARGE_LEVEL)
        return self.batterie.u_soc

    def get_operating_mode(self) -> int:
        return self.batterie.configuration_em_operatingmode #get_configuration(SONNEN_CONFIGURATION_OPERATING_MODE)

    def get_operating_mode_name(self) -> str:
    #    operating_mode_num = self.get_operating_mode()
        return self.batterie.configuration_em_operatingmode_name  #SONNEN_OPERATING_MODES_TO_OPERATING_MODE_NAMES.get(operating_mode_num)

    # def set_operating_mode(self, operating_mode):
    #     return self.set_configuration(SONNEN_CONFIGURATION_OPERATING_MODE, operating_mode)

    # def set_operating_mode_by_name(self, operating_mode_name):
    #     return self.set_operating_mode(SONNEN_OPERATING_MODE_NAMES_TO_OPERATING_MODES.get(operating_mode_name))

    def get_battery_reserve(self) -> int:
        return self.batterie.configuration_em_usoc #get_configuration(SONNEN_CONFIGURATION_BACKUP_RESERVE)

    # def set_battery_reserve(self, reserve=5):
    #     reserve = int(reserve)
    #     if (reserve < 0) or (reserve > 100):
    #         raise Exception("Reserve must be between 0 and 100, you specified "+reserve)
    #     return self.set_configuration(SONNEN_CONFIGURATION_BACKUP_RESERVE, reserve)

    # set the reserve to the current battery level adjusted by the offset if provided
    # (a positive offset means that the reserve will be set to more than the current level
    # a negative offser means less than the current level)
    # If the new reserve is less than the minimum reserve then use the minimum reserve
    # the reserve will be tested to ensure it's >= 0 or <= 100

    # def set_battery_reserve_relative_to_currentCharge(self, offset=0, minimum_reserve=0):
    #     current_level = self.get_current_charge_level()
    #     target_level = current_level +offset
    #     if (target_level <  minimum_reserve):
    #         target_level = minimum_reserve
    #     if (target_level < 0) :
    #         target_level = 0
    #     elif (target_level > 100):
    #         target_level = 100
    #     return self.set_battery_reserve(target_level)

    def get_time_of_use_schedule_as_string(self) -> str:
        """Config param is a <List>
            Return:
                JSON string of the List
        """
        return json.dumps(self.get_configuration(SONNEN_CONFIGURATION_TOU_SCHEDULE))

    def get_time_of_use_schedule_as_json_objects(self) -> Dict:
        return json.loads(self.get_time_of_use_schedule_as_string())

    def get_time_of_use_schedule_as_schedule(self)-> timeofuseschedule:
        current_schedule = self.get_configuration(SONNEN_CONFIGURATION_TOU_SCHEDULE) #is List
        return timeofuseschedule.build_from_json(current_schedule)

    # In this case the schedule is a array representation of an array of dictionary formatted time of use entries, each entry has a start time and stop time and a threshold_p_max (max grid power for the entire building including charging)
    # async def set_time_of_use_schedule_from_json_objects(self, schedule):
    #     return self.set_configuration(SONNEN_CONFIGURATION_TOU_SCHEDULE, json.dumps(schedule))