from sensors.DistanceSensor import DistanceSensor
import time, datetime
import json
import os, errno
import logging, traceback

def main():

    # Set logger
    setLogger()

    # Run time in seconds
    minRunTimeSecs = 1
    runCount = 0
    maxRunCount = 1

    print("Start of distance sensor")
    # Recover from collection errors - unless repeated quickly
    while True:
        startTime = time.time()
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

    sensorWaitTime = 0.05
    dataPerWrite = 50
    fileCount = 0
    dataCollectionCount = 0
    sensorData = {}

    # Create file for data
    dirName = createDirectory(saveLocation)
    sensors = createSensors()

    # Data collection
    # TODO Replace with Async data collection
    while (True):

        # Collect data and input into sensorData
        sensorData = {**sensorData, **collectSensorData(sensors)}
        dataCollectionCount += 1

        # Store data in local file
        if (sensorDataCount > dataPerWrite):
            print(sensorDataCount / (time.time() - startTime), " recordings a second.") 
            fileCount += 1
            writeDataToFile(sensorData, dirName, fileCount)
            sensorDataCount = 0
            sensorData = {}

def collectSensorData(sensors):
    sensorData = {}
    for i in sensors:
        data = i.getData()
        sensorData[data["time"]] =  data
        sensorDataCount += 1
        time.sleep(sensorWaitTime)

    return sensorData

def createSensors():

    sensors = []
    # TODO Sensors should be generated from config file
    sensors.append(DistanceSensor("Sensor1",16,19))
    #sensor2.append(DistanceSensor("Sensor2",20,26))

    return sensors

def writeDataToFile(data, dirName, fileCount):
    fileName = "data/" + dirName + "/data" + str(fileCount) + ".json" 
    with open(fileName, 'w+') as fp:
        json.dump(data, fp)

def createDirectory(saveLocation):

    existingFiles = os.listdir(saveLocation)
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
    logging.basicConfig(filename='collectSesnorData.log',level=logging.DEBUG)
    logging.info('Start of logs. Time={}'.format(time.ctime()))

if __name__ == "__main__":

    print("Start")
    # main()
