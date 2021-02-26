class create_prtg_json:
    """Takes the required inputted values and puts them into the JSON template"""
    def __init__(self, temperature, pressure, amblight):
        self.temperature = temperature
        self.pressure = pressure
        self.amblight = amblight

    def create_json(self):
        json_response = {
        "prtg": {
            "result": [
                {
                    "channel": "temperature",
                    "float": 1,
                    "value": {}
                },
                {
                    "channel": "pressure",
                    "float": 1,
                    "value": {}
                },
                {
                    "channel": "ambient light",
                    "float": 1,
                    "value": {}
                }
            ]
        }
    }
    