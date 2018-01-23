from sensors.EchoSensor import EchoSensor
from utlis.utilities import writeDataToFile, createDirectory
import time, datetime
import os, sys, errno
import logging, traceback

def main():

    # Script path
    path =  os.path.dirname(os.path.realpath(__file__)) + "/../"
    # Set logger
    setLogger(path)

    # Run time in seconds
    minRunTimeSecs = 1
    runCount = 0
    maxRunCount = 1

    print("Start of distance sensor")
    startTime = time.time()

    # Recover from collection errors - unless repeated quickly
    while True:
        if (runCount > maxRunCount):
            break
        try:
            collectAndStoreData(path)
        except Exception as e:
            runTime = time.time() - startTime
            logging.info('\n')
            logging.debug('Ran for {} seconds. Current time={}'.format(runTime, time.ctime()))
            logging.debug('Message {}'.format(str(e)))
            logging.exception("Excpetion in main.")
            startTime = time.time()
        if (runTime < minRunTimeSecs):
            logging.debug('Exited as run time is too short. Current time={}'.format(time.ctime()))
            break

def collectAndStoreData(path, saveLocation="data"):

    saveLocation = path + saveLocation

    # Collection varibles
    sensorWaitTime = 0.005
    dataPerWrite = 50
    fileCount = 0
    dataCollectionCount = 0
    sensorData = {}

    # Create file for data
    dirName = createDirectory(saveLocation)
    sensors = createSensors()

    # Data collection
    # TODO Replace with Async data collection
    startTime = time.time()
    while (True):

        # Collect data and input into sensorData
        sensorData = {**sensorData, **collectSensorData(sensors, sensorWaitTime)}
        dataCollectionCount += 1

        # Store data in local file
        if (dataCollectionCount > dataPerWrite):
            print(dataCollectionCount / (time.time() - startTime), " recordings a second. \n") 
            fileCount += 1
            # print(sensorData)
            for i in sensorData:
                print(sensorData.get(i))
            writeDataToFile(path, sensorData, dirName, fileCount)
            dataCollectionCount = 0
            sensorData = {}
            startTime = time.time()

def collectSensorData(sensors, sensorWaitTime):
    sensorData = {}
    for i in sensors:
        data = i.getData()
        sensorData[data["time"]] =  data
        time.sleep(sensorWaitTime)

    return sensorData

def createSensors():

    sensors = []
    # TODO Sensors should be generated from config file
    sensors.append(EchoSensor("Sensor1",16,19))
    sensors.append(EchoSensor("Sensor2",20,26))

    return sensors

def setLogger(path):
    fileName = path + "logs/collectSensorData.log"
    logging.basicConfig(filename=fileName, level=logging.DEBUG)
    logging.info('Start of logs. Time={}'.format(time.ctime()))

if __name__ == "__main__":

    print("Start sensor running")
    main()
