import json

def writeDataToFile(data, dirName, fileCount):
    fileName = "data/" + dirName + "/data" + str(fileCount) + ".json" 
    with open(fileName, 'w+') as fp:
        json.dump(data, fp)

if (__name__ == '__main__'):

    print("Utilites")