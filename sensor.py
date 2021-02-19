from configparser import ConfigParser
import requests
import time
import logging
import serial
import sys
from serial.serialutil import Timeout
from envirophat import weather,light

config_object = ConfigParser()
config_object.read("config.ini")

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
    global temperature
    global pressure
    global amblight

    temperature = weather.temperature()
    pressure = round(weather.pressure(), 2)
    amblight = light.light()

    json_response = {
        "prtg": {
            "result": [
                {
                    "channel": "temperature",
                    "float": 1,
                    "value": temperature
                },
                {
                    "channel": "pressure",
                    "float": 1,
                    "value": pressure
                },
                {
                    "channel": "ambient light",
                    "float": 1,
                    "value": amblight
                }
            ]
        }
    }
    return json_response

def clearscreen():
    clearchars = [chr(254),chr(88)]
    for i in clearchars:
        port.write(i)

def send_to_lcd(temp,press,ambientlight):
    message1 = "Temperature: {}".format(temp)
    message2 = "Pressure: {}".format(press)
    message3 = "Light: {}".format(ambientlight)

    clearscreen()
    port.write(message1) 
    time.sleep(10)

    clearscreen()
    port.write(message2)
    time.sleep(10)

    clearscreen()
    port.write(message3)
    time.sleep(10)

monitorconfig = config_object["MONITORCONFIG"]
prtgconfig = config_object["PRTGCONFIG"]

port = serial.Serial(8, 19200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=5, rtscts=False)

logtime = str.replace(str(time.time()), ".", "-")
logging.basicConfig(filename="logfilename" + logtime + ".log", level=logging.INFO)

logging.info("""Starting Sensor

Current Unix Epoch Time: 
{}

Current config.ini file:
{}
""").format(logtime, config_read())

try: 
    while True:
        try:
            json_response = get_values()
            json_string = str(json_response)
            json_string = str.replace(json_string, '\'', '\"')
            prtg_request_URL = 'https://' + prtgconfig["prtgserverip"] + ':' + prtgconfig["prtgserverport"] + '/' + prtgconfig["prtgsensortoken"] + "?content=" + json_string
            if str(monitorconfig['enabledebuglogging']) == '1':
                logging.debug(json_response)
                logging.debug(json_string)
                logging.debug(prtg_request_URL)
            else:
                pass
            request = requests.get(prtg_request_URL)
            if str(monitorconfig['enabledebuglogging']) == '1':
                logging.debug(request.status_code)
            
        except:
            
            pass
        time.sleep(int(prtgconfig["datasendinterval"]))

except KeyboardInterrupt:
    pass