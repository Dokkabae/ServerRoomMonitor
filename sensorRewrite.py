from configparser import ConfigParser
import requests
import time
import logging
import serial
import sys
from serial.serialutil import Timeout
from envirophat import weather,temperature

config_object = ConfigParser()
config_object.read("config.ini")

monitorconfig = config_object["MONITORCONFIG"]
prtgconfig = config_object["PRTGCONFIG"]

## Do not change these functions. All changes should be done in the config file!

def config_read():
    with open("config.ini", "rt") as config:
        current_config = config.read()
    return current_config

def check_config():
    try: 
        chkconfigdata = int(prtgconfig["datasendinterval"])

    except:
        logging.exception("datasendinterval cannot be a non integer!")
        sys.exit()

def get_values():
    # Creates the JSON values that are sent to PRTG
    global temperature

    temperature = weather.temperature()

    json_response = {
        "prtg": {
            "result": [
                {
                    "channel": "temperature",
                    "float": 1,
                    "value": temperature
                }
            ]
        }
    }
    return json_response