import json
from pprint import pprint
# from dateutil.parser import parse
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import os

def loadData(dirName):
    data = []
    files = os.listdir(dirName)
    for i in files:
        curFile = dirName + "/" + i
        try:
            with open(curFile) as json_data:
                d = json.load(json_data)
                data.append(d)
        except Exception as e:
            print(curFile, " failed to load")
    return data

def prepareDateForPlot(singleSensorData):
    sortedData = sorted(singleSensorData, key=lambda x: x[0])

    x = []
    y = []

    # Clean data
    for i in sortedData:
        if (i[1] != 1000 and i[1] > 0):
            x.append(i[0])
            y.append(i[1])

    return [x,y]

def convertEpoc(timeStamp):
    return datetime.fromtimestamp(timeStamp)

def main(folder):

    data = loadData("data/" + folder)

    dateTimeStamps = []
    ses1 = []
    ses2 = []

    # Extract data 
    for dic in data:
        for k,v in dic.items():
            if (dic[k]["sensorName"] == "Sensor1"):
                timeStamp = float(dic[k]['time'])
                date = convertEpoc(timeStamp)
                distance = dic[k]["distance"]

                ses1.append([date,distance])
                dateTimeStamps.append(timeStamp)
            else:
                timeStamp = float(dic[k]['time'])
                date = convertEpoc(timeStamp)
                distance = dic[k]["distance"]

                ses2.append([date,distance])
                dateTimeStamps.append(timeStamp)

    sensorData = prepareDateForPlot(ses1)
    s2 = prepareDateForPlot(ses2)

    # Add data to plot
    plt.scatter(sensorData[0], sensorData[1])
    plt.scatter(s2[0],s2[1])

    # Set min max
    xmin = min(dateTimeStamps) 
    xmax = max(dateTimeStamps)
    delta = (xmax- xmin) * 0.05
    xmin = convertEpoc(xmin - delta)
    xmax = convertEpoc(xmax + delta)
    plt.xlim(xmin, xmax)

    plt.show()

if __name__ == "__main__":

    print("Displaying data")
    folder = input("Name of folder to extra data from? \n")
    main(folder)