from sensors.EchoSensor import EchoSensor
from utlis.utilities import writeDataToFile
import time, datetime
import os, sys, errno
import logging, traceback

def main():

    # Set logger
    setLogger()

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
            collectAndStoreData()
        except Exception as e:
            runTime = time.time() - startTime
            logging.debug('Ran for {} seconds. Current time={}'.format(runTime, time.ctime()))
            logging.debug('Trace {}'.format(traceback.print_exc(), ))
        if (runTime < minRunTimeSecs):
            logging.debug('Exited as run time is too short. Current time={}'.format(time.ctime()))
            break

def collectAndStoreData(saveLocation="data"):

    sensorWaitTime = 0.01
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
            print(sensorData)
            writeDataToFile(sensorData, dirName, fileCount)
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
    #sensors.append(EchoSensor("Sensor2",20,26))

    return sensors


def createDirectory(saveLocation):

    existingFiles = os.listdir(saveLocation)
    if "README.md" in existingFiles:
        existingFiles.remove("README.md")

    if len(existingFiles) == 0:
        newDir = "data1"
    else:
        newDir = "data" + str(max([int(x.split("a")[2]) for x in existingFiles])+1)
    try:
        os.makedirs(saveLocation + "/" + newDir)
    except OSError as exception:
        logging.debug('Error - {} \n Current time={}'.format(raceback.print_exc(), time.ctime()))
        # logging.info("Setting data directory as current")
        # TODO Create new directroy for savaing data
        raise exception
    return newDir

def setLogger():
    fileName = "logs/collectSensorData.log"
    logging.basicConfig(filename=fileName, level=logging.DEBUG)
    logging.info('Start of logs. Time={}'.format(time.ctime()))

if __name__ == "__main__":

    print("Start sensor running")
    main()
