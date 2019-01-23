import requests
import json
import numpy as np

url = 'http://api.luftdaten.info/static/v2/data.24h.json'
air_request = requests.get(url, verify = True)

# For successful API call, response code will be 200 (OK)
if (air_request.ok):
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    api_data = [{}]
    jData = json.loads(air_request.content)
    print(jData)
#Use numpy array to get the location values of each sensor and check if it is in the Sofia area, sofia_radius = 9km
    #print(json.dumps(jData, indent=4, sort_keys=True))

else:
  # If response code is not ok (200), print the resulting http error code with description
    air_request.raise_for_status()


