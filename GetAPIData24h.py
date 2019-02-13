#
# Fetching and extracting data from JSON using the luftdaten API
#

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize


def getRequest(url):
    air_response = requests.get(url, verify=True)
    json_data = []
    json_data2 = []

    # For successful API call, response code will be 200 (OK)
    if (air_response.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        json_data = json.loads(air_response.content)
        json_data2 = air_response.json()

    else:
        # If response code is not ok (200), print the resulting http error code with description
        air_response.raise_for_status()

    return json_data, air_response, json_data2


#Normalize the list of dictionaries received from the request
def normalize(json_data):
    normal_data = pd.io.json.json_normalize(json_data)

    return normal_data

#Extract timestamp from normalized data
def extractTime_Location(data):
    timelocation_data = data[["timestamp", "location.latitude", "location.longitude"]]

    return timelocation_data

#Extract sensor values from normalized data
def extractSensorValues(data):
    sensor_values = data[["sensordatavalues"]]

    return sensor_values

#Transform sensor values pd to dictionary
def dataframe_to_dictionary(dataframe):
    sensor_data_dict = dataframe.to_dict(orient="records")

    return sensor_data_dict


#Write Dataframe to exel file
def dataFrametoExel(dataframe, filename):
    writer = pd.ExcelWriter(filename)
    dataframe.to_excel(writer, index=False)
    writer.save()

def main():
    # define a variable to hold the source URL
    luftdaten_API_url = 'http://api.luftdaten.info/static/v2/data.24h.json'

    # # Open the URL and read the data
    # webUrl = urllib.request.urlopen(urlData)
    # print("result code: " + str(webUrl.getcode()))
    # if (webUrl.getcode() == 200):
    #     data = webUrl.read()
    #     # print out our customized results
    #     printResults(data)
    # else:
    #     print("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))

    #get data from json
    json_data, air_response, json_data2 = getRequest(luftdaten_API_url)

    #normalize all the data
    normal_data = normalize(json_data)

    #extract sensor data
    sensor_data = extractSensorValues(normal_data)
    
    # sensor_a = pd.concat([pd.DataFrame(x) for x in sensor_data['sensordatavalues']]).reset_index(level=0, drop=True)
    # print(sensor_a)

    #transform sendor dataframe to dictionary
    sensor_dict = (dataframe_to_dictionary(sensor_data))

#normalize the sensor data transformed to dictionary
    normal_sensor_data = normalize(sensor_dict)
    print(normal_sensor_data==sensor_data)


#extract time and location
    extractTime_Location()

    #save to exel
    dataFrametoExel(normal_sensor_data, 'sensor.xlsx')

if __name__ == "__main__":
    main()
