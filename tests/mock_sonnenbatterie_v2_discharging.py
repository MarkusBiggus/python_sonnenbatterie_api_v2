"""Mock batterie data also used in package sonnenbatterie_api_v2 & ha component sonnenenbatterie
    Discharging above reserve (OnGrid)
"""
import json
def __mock_status_discharging(*args)-> json:
    return {
        'Apparent_output': 1438,
        'BackupBuffer': '20',
        'BatteryCharging': False,
        'BatteryDischarging': True,
        'Consumption_Avg': 1563,
        'Consumption_W': 1541,
        'Fac': 50.0167121887207,
        'FlowConsumptionBattery': True,
        'FlowConsumptionGrid': False,
        'FlowConsumptionProduction': True,
        'FlowGridBattery': False,
        'FlowProductionBattery': False,
        'FlowProductionGrid': False,
        'GridFeedIn_W': 0,
        'IsSystemInstalled': 1,
        'OperatingMode': '2',
        'Pac_total_W': 1438,
        'Production_W': 103,
        'RSOC': 88,
        'RemainingCapacity_Wh': 40181,
        'Sac1': 438,
        'Sac2': None,
        'Sac3': None,
        'SystemStatus': 'OnGrid',
        'Timestamp': '2023-11-20 17:00:58',
        'USOC': 88,
        'Uac': 237,
        'Ubat': 211,
        'dischargeNotAllowed': False,
        'generator_autostart': False
    }

def __mock_latest_discharging(*args)-> json:
    return {
        'FullChargeCapacity': 20683.490,
        'GridFeedIn_W': 0,
        'Pac_total_W': 1438,
        'Consumption_W': 1541,
        'Production_W': 103,
        'RSOC': 88,
        'SetPoint_W': 439,
        'Timestamp': '2023-11-20 17:00:58',
        'USOC': 88,
        'UTC_Offet': 2,
        'ic_status': {
            'DC Shutdown Reason': {
                'Critical BMS Alarm': False,
                'Electrolyte Leakage': False,
                'Error condition in BMS initialization': False,
                'HW_Shutdown': False,
                'HardWire Over Voltage': False,
                'HardWired Dry Signal A': False,
                'HardWired Under Voltage': False,
                'Holding Circuit Error': False,
                'Initialization Timeout': False,
                'Initialization of AC contactor failed': False,
                'Initialization of BMS hardware failed': False,
                'Initialization of DC contactor failed': False,
                'Initialization of Inverter failed': False,
                'Invalid or no SystemType was set': False,
                'Inverter Over Temperature': False,
                'Inverter Under Voltage': False,
                'Inverter Version Too Low For Dc-Module': False,
                'Manual shutdown by user': False,
                'Minimum rSOC of System reached': False,
                'Modules voltage out of range': False,
                'No Setpoint received by HC': False,
                'Odd number of battery modules': False,
                'One single module detected and module voltage is out of range': False,
                'Only one single module detected': False,
                'Shutdown Timer started': False,
                'System Validation failed': False,
                'Voltage Monitor Changed': False
            },
            'Eclipse Led': {
                'Blinking Red': False,
                'Pulsing Green': False,
                'Pulsing Orange': False,
                'Pulsing White': True,
                'Solid Red': False
            },
            'MISC Status Bits': {
                'Discharge not allowed': False,
                'F1 open': False,
                'Min System SOC': False,
                'Min User SOC': False,
                'Setpoint Timeout': False
            },
            'Microgrid Status': {
                'Continious Power Violation': False,
                'Discharge Current Limit Violation': False,
                'Low Temperature': False,
                'Max System SOC': False,
                'Max User SOC': False,
                'Microgrid Enabled': False,
                'Min System SOC': False,
                'Min User SOC': False,
                'Over Charge Current': False,
                'Over Discharge Current': False,
                'Peak Power Violation': False,
                'Protect is activated': False,
                'Transition to Ongrid Pending': False
            },
            'Setpoint Priority': {
                'BMS': False,
                'Energy Manager': True,
                'Full Charge Request': False,
                'Inverter': False,
                'Min User SOC': False,
                'Trickle Charge': False
            },
            'System Validation': {
                'Country Code Set status flag 1': False,
                'Country Code Set status flag 2': False,
                'Self test Error DC Wiring': False,
                'Self test Postponed': False,
                'Self test Precondition not met': False,
                'Self test Running': False,
                'Self test successful finished': False
            },
            'nrbatterymodules': 4,
            'secondssincefullcharge': 574,
            'statebms': 'ready',
            'statecorecontrolmodule': 'ongrid',
            'stateinverter': 'running',
            'timestamp': 'Mon Nov 20 17:00:58 2023'
        }
    }

def __mock_inverter_discharging(*args)-> json:
    return {
        "fac": 0.0,
        "iac_total": 0.39,
        "ibat": 0.01,
        "ipv": 0.0,
        "pac_microgrid": 0.0,
        "pac_total": 1438,
        "pbat": -0.14,
        "phi": -0.82,
        "ppv": 0.0,
        "sac_total": 0.0,
        "tmax": 55.53,
        "uac": 233.55,
        "ubat": 209.18,
        "upv": 0.0
    }