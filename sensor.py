from configparser import ConfigParser
import os
import requests
import time
import logging
from envirophat import weather,light

config_object = ConfigParser()
config_object.read("config.ini")

monitorconfig = config_object["MONITORCONFIG"]
prtgconfig = config_object["PRTGCONFIG"]

logtime = str.replace(str(time.time()), ".", "-")
logging.basicConfig(filename="logfilename" + logtime + ".log", level=logging.INFO)

logging.info("""Starting Sensor

Current Unix Epoch Time: 
{}

Current Config Settings:
Monitor Config
Data send interval: {} seconds

PRTG Config
""").format(logtime, monitorconfig["datasendinterval"])

def get_values():
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

try: 
    while True:
        try:
            json_response = get_values()
            json_string = str(json_response)
            json_string = str.replace(json_string, '\'', '\"')
            prtg_request_URL = 'https://' + prtgconfig["prtgserverhost"] + ':' + prtgconfig["prtgserverport"] + '/' + prtgconfig["prtgsensortoken"] + "?content=" + json_string
            if str(monitorconfig['debugenabled']) == '1':
                logging.debug(json_response)
                logging.debug(json_string)
                logging.debug(prtg_request_URL)
            else:
                pass
            request = requests.get(prtg_request_URL)
            if str(monitorconfig['debugenabled']) == '1':
                logging.debug(request.status_code)
            
        except:
            
            pass
        time.sleep(int(prtgconfig["datasendinterval"]))

except KeyboardInterrupt:
    pass