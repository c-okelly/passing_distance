import json, os

def writeDataToFile(path, data, dirName, fileCount):
    fileName = path + "data/" + dirName + "/data" + str(fileCount) + ".json" 
    with open(fileName, 'w+') as fp:
        json.dump(data, fp)

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
        logging.debug('Error - {} \n Current time={}'.format(str(e), time.ctime()))
        logging.exception("Error creating file.")
        raise exception
    return newDir

if (__name__ == '__main__'):

    print("Utilites")