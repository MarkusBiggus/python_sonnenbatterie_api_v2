"""Mock batterie data also used in package sonnenbatterie_api_v2 & ha component sonnenenbatterie"""
import json
def __mock_status_charging(*args)-> json:
    return {
        'Apparent_output': 98,
        'BackupBuffer': '20',
        'BatteryCharging': True,
        'BatteryDischarging': False,
        'Consumption_Avg': 486,
        'Consumption_W': 1578,
        'Fac': 50.05781555175781,
        'FlowConsumptionBattery': False,
        'FlowConsumptionGrid': False,
        'FlowConsumptionProduction': True,
        'FlowGridBattery': False,
        'FlowProductionBattery': True,
        'FlowProductionGrid': False,
        'GridFeedIn_W': 0,
        'IsSystemInstalled': 1,
        'OperatingMode': '2',
        'Pac_total_W': -1394,
        'Production_W': 2972,
        'RSOC': 88,
        'RemainingCapacity_Wh': 40181,
        'Sac1': 99,
        'Sac2': None,
        'Sac3': None,
        'SystemStatus': 'OnGrid',
        'Timestamp': '2023-11-20 17:00:55',
        'USOC': 81,
        'Uac': 235,
        'Ubat': 212,
        'dischargeNotAllowed': False,
        'generator_autostart': False
    }

def __mock_latest_charging(*args)-> json:
    return {
        'FullChargeCapacity': 20187.086,
        'GridFeedIn_W': 0,
        'Production_W': 2972,
        'Consumption_W': 1578,
        'Pac_total_W': -1394,
        'RSOC': 88,
        'SetPoint_W': -145,
        'Timestamp': '2023-11-20 17:00:55',
        'USOC': 81,
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
                "Brightness":100,
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
            'secondssincefullcharge': 3720,
            'statebms': 'ready',
            'statecorecontrolmodule': 'ongrid',
            'stateinverter': 'running',
            'timestamp': 'Mon Nov 20 17:00:55 2023'
        }
    }

def __mock_configurations(*args)-> json:
# Economical Charging (default)
    return {
        "EM_RE_ENABLE_MICROGRID": 'False',
        "NVM_PfcIsFixedCosPhiActive": 0,
        "NVM_PfcFixedCosPhi": 0.8,
        "IC_BatteryModules": 4,
        "EM_ToU_Schedule": [],
        "DE_Software":"1.14.5",
        "EM_USER_INPUT_TIME_ONE": 0,
        "NVM_PfcIsFixedCosPhiLagging": 0,
        "EM_Prognosis_Charging": 1,
        "EM_USOC": 20,
        "EM_USER_INPUT_TIME_TWO": 0,
        "EM_OperatingMode": "2",
        "SH_HeaterTemperatureMax": 80,
        "SH_HeaterOperatingMode": 0,
        "IC_InverterMaxPower_w": 5000,
        "SH_HeaterTemperatureMin": 0 ,
        "CM_MarketingModuleCapacity": 5000,
        "EM_USER_INPUT_TIME_THREE": 0,
        "CN_CascadingRole": "none",
        "EM_US_GEN_POWER_SET_POINT": 0,
        "DepthOfDischargeLimit": 93
    }

def __mock_battery(*args)-> json:
    return {
        "balancechargerequest":0.0,
        "chargecurrentlimit":39.97,
        "cyclecount":30.0,
        "dischargecurrentlimit":39.97,
        "fullchargecapacity":201.98,
        "fullchargecapacitywh":20683.490,
        "maximumcelltemperature":19.95,
        "maximumcellvoltage":3.257,
        "maximumcellvoltagenum":0.0,
        "maximummodulecurrent":0.0,
        "maximummoduledcvoltage":104.15,
        "maximummoduletemperature":-273.15,
        "minimumcelltemperature":18.95,
        "minimumcellvoltage":3.251,
        "minimumcellvoltagenum":0.0,
        "minimummodulecurrent":0.0,
        "minimummoduledcvoltage":104.15,
        "minimummoduletemperature":-273.15,
        "nominalmoduledcvoltage":102.4,
        "relativestateofcharge":88.0,
        "remainingcapacity":177.74,
        "systemalarm":0.0,
        "systemaveragecurrent":0.035,
        "systemcurrent":0.0,
        "systemdcvoltage":208.3,
        "systemstatus":88.0,
        "systemtime":0.0,
        "systemwarning":0.0,
        "usableremainingcapacity":163.60
    }

def __mock_powermeter(*args)-> json:
    return [
        {
            'a_l1': 2.4730000495910645,
            'a_l2': 0,
            'a_l3': 0,
            'channel': 1,
            'deviceid': 4,
            'direction': 'production',
            'error': 0,
            'kwh_exported': 0,
            'kwh_imported': 3969.800048828125,
            'v_l1_l2': 0,
            'v_l1_n': 246.60000610351562,
            'v_l2_l3': 0,
            'v_l2_n': 0,
            'v_l3_l1': 0,
            'v_l3_n': 0,
            'va_total': 609.5,
            'var_total': 0,
            'w_l1': 609.5,
            'w_l2': 0,
            'w_l3': 0,
            'w_total': 609.5
        },
        {
            'a_l1': 2.0929999351501465,
            'a_l2': 0,
            'a_l3': 0,
            'channel': 2,
            'deviceid': 4,
            'direction': 'consumption',
            'error': 0,
            'kwh_exported': 0,
            'kwh_imported': 816.5,
            'v_l1_l2': 0,
            'v_l1_n': 246.6999969482422,
            'v_l2_l3': 0,
            'v_l2_n': 0,
            'v_l3_l1': 0,
            'v_l3_n': 0,
            'va_total': 516.2000122070312,
            'var_total': -512.7999877929688,
            'w_l1': 59.29999923706055,
            'w_l2': 0,
            'w_l3': 0,
            'w_total': 59.29999923706055
        }
    ]

def __mock_inverter(*args)-> json:
    return {
        "fac": 0.0,
        "iac_total": 0.39,
        "ibat": 0.01,
        "ipv": 0.0,
        "pac_microgrid": 0.0,
        "pac_total": -1394.33,
        "pbat": -0.14,
        "phi": -0.82,
        "ppv": 0.0,
        "sac_total": 0.0,
        "tmax": 55.53,
        "uac": 233.55,
        "ubat": 209.18,
        "upv": 0.0
    }