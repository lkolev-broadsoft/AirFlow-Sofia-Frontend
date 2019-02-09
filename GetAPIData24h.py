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



# def printResults(data):
#     # Use the json module to load the string data into a dictionary
#     theJSON = json.loads(data)
#
#     # now we can access the contents of the JSON like any other Python object
#     if "title" in theJSON["metadata"]:
#         print(theJSON["metadata"]["title"])
#
#     # output the number of events, plus the magnitude and each event name
#     count = theJSON["metadata"]["count"];
#     print(str(count) + " events recorded")
#
#     # for each event, print the place where it occurred
#     for i in theJSON["features"]:
#         print(i["properties"]["place"])
#     print("--------------\n")
#
#     # print the events that only have a magnitude greater than 4
#     for i in theJSON["features"]:
#         if i["properties"]["mag"] >= 4.0:
#             print("%2.1f" % i["properties"]["mag"], i["properties"]["place"])
#     print("--------------\n")
#
#     # print only the events where at least 1 person reported feeling something
#     print("\n\nEvents that were felt:")
#     for i in theJSON["features"]:
#         feltReports = i["properties"]["felt"]
#         if (feltReports != None):
#             if (feltReports > 0):
#                 print("%2.1f" % i["properties"]["mag"], i["properties"]["place"],
#                       " reported " + str(feltReports) + " times")


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
