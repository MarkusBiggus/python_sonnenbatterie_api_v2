"""Verify package sonnenbatterie V2 API used by sonnenbatterie component works."""
"""pytest test/test_battery_devinfo.py -s -v -x """
import os
import pytest

from dotenv import load_dotenv
from sonnenbatterie import sonnenbatterie

DOMAIN = "sonnenbatterie" # from sonnenbatterie.const import

load_dotenv()

BATTERIE_HOST = os.getenv("BATTERIE_HOST", "X")
API_READ_TOKEN = os.getenv("API_READ_TOKEN", "X")
API_WRITE_TOKEN = os.getenv("API_WRITE_TOKEN", "X")

if BATTERIE_HOST == "X" or (API_WRITE_TOKEN == "X" and API_READ_TOKEN == "X"):
    print(f"host: {BATTERIE_HOST} WRITE: {API_WRITE_TOKEN} READ: {API_READ_TOKEN}")
    raise ValueError(
        "Set BATTERIE_HOST & API_READ_TOKEN or API_WRITE_TOKEN in .env See env.example"
    )


def test_devinfo() -> None:
    _battery = sonnenbatterie(
        "", API_WRITE_TOKEN if API_WRITE_TOKEN != "X" else API_READ_TOKEN, BATTERIE_HOST
    )
    assert _battery is not False
    system_data = _battery.get_systemdata()
    #print(f'system_data type: {type(system_data)}')
    model = system_data.get("ERP_ArticleName", "unknown")
    name=f"{DOMAIN} {system_data.get('DE_Ticket_Number', 'unknown')}"
    sw_version = system_data.get("software_version", "unknown")
    print(f"model: {model}  name: {name}  sw_version: {sw_version}")
    assert system_data.get('DE_Ticket_Number') == 'unknown'

def test_batterysystem() -> None:
    _battery = sonnenbatterie(
        "", API_WRITE_TOKEN if API_WRITE_TOKEN != "X" else API_READ_TOKEN, BATTERIE_HOST
    )
    assert _battery is not False
    latestData = {}
    # code syntax from custom_component coordinator.py
    latestData["battery_system"] = _battery.get_batterysystem()
    print(f'latest: {latestData}')
    batt_module_capacity = int(
        latestData["battery_system"]["battery_system"]["system"][
            "storage_capacity_per_module"
        ]
    )
    assert batt_module_capacity == 5000
    batt_module_count = int(latestData["battery_system"]["modules"])
    assert batt_module_count == 2

def test_powermeter() -> None:
    _battery = sonnenbatterie(
        "", API_WRITE_TOKEN if API_WRITE_TOKEN != "X" else API_READ_TOKEN, BATTERIE_HOST
    )
    assert _battery is not False
    latestData = {}
    # code syntax from custom_component coordinator.py
    latestData["powermeter"] = _battery.get_powermeter()
    #print(f'powermeter type: {type(latestData["powermeter"])}')
    if(isinstance(latestData["powermeter"],dict)):
        newPowerMeters=[]
        for index,dictIndex in enumerate(latestData["powermeter"]):
            newPowerMeters.append(latestData["powermeter"][dictIndex])
        print(f'new powermeters: {newPowerMeters}')

def test_status() -> None:
    _battery = sonnenbatterie(
        "", API_WRITE_TOKEN if API_WRITE_TOKEN != "X" else API_READ_TOKEN, BATTERIE_HOST
    )
    assert _battery is not False
    latestData = {}
    # code syntax from custom_component coordinator.py
    latestData["status"] = _battery.get_status()
    #print(f'status type: {type(latestData["status"])}')
    latestData["battery_info"] = _battery.get_battery()
    #print(f'status type: {type(latestData["battery_info"])}')
    #print(f'{latestData}')
    # if latestData["status"]["BatteryCharging"]:
    #     battery_current_state = "charging"
    # elif latestData["status"]["BatteryDischarging"]:
    #     battery_current_state = "discharging"
    # else:
    #     battery_current_state = "standby"
    battery_current_state = latestData["battery_info"].get('current_state')
    #print(f'{latestData["battery_info"]}')
    rsoc = latestData["battery_info"].get('relativestateofcharge')
    systemstatus = latestData["battery_info"].get('systemstatus')
    health = latestData["battery_info"].get('measurements').get('battery_status').get('stateofhealth')
    print(f'battery_state: {battery_current_state}  RSOC: {rsoc}%')
    assert health == systemstatus

def test_batteryinfo() -> None:
    _battery = sonnenbatterie(
        "", API_WRITE_TOKEN if API_WRITE_TOKEN != "X" else API_READ_TOKEN, BATTERIE_HOST
    )
    assert _battery is not False
    latestData = {}
    # code syntax from custom_component coordinator.py
        # fixed value, percentage of total installed power reserved for
        # internal battery system purposes

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
