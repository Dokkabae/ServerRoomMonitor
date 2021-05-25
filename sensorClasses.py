class toJson:
    """Takes inputted values and converts them into PRTGs JSON formal"""
    def __init__(self, temperature):
        self.temperature = temperature

    json_response = {
        "prtg": {
            "result": [
                {
                    "channel": "temperature",
                    "float": 1,
                    "value": {}
                }
            ]
        }
    }

