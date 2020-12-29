from configparser import ConfigParser
import os
import requests
import time
from envirophat import weather,light

config_object = ConfigParser()
config_object.read("config.ini")

monitorconfig = config_object["MONITORCONFIG"]
prtgconfig = config_object["PRTGCONFIG"]

print("Starting Sensor")
print("")
print("Current Config Settings:")
print("Monitor Config")
print("Data send interval: {} seconds").format(monitorconfig["datasendinterval"])
print("")
print("PRTG Config")
print("")

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
                print(json_response)
                print(json_string)
                print(prtg_request_URL)
            else:
                pass
            request = requests.get(prtg_request_URL)
            if str(monitorconfig['debugenabled']) == '1':
                print(request.status_code)
            
        except:
            pass
        time.sleep(prtgconfig["datasendinterval"])

except KeyboardInterrupt:
    pass