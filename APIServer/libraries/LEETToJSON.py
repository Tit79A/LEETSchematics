import os
import json
from libraries import GlobalTools
from _collections import OrderedDict


maxSize = 400000


def generateFiles(token, size):
    outputData = {}
    outputData["width"], outputData["height"], outputData["length"] = size
    outputData["blocks"] = []
    
    try:
        outputFile = open("../output/json/" + token + ".json", "w")
        outputFile.write(json.dumps(outputData))
        outputFile.close()
        
        open("../output/temp/" + token + ".temp", "a").close()
        return True
    except:
        return False


def NewSchematicHandler(parameters):
    if len(parameters) >= 1:
        if GlobalTools.canStringArrayBePositiveIntArray(parameters[0].split(",")):
            size = list(map(int, parameters[0].split(",")))
            if len(size) == 3:
                token = GlobalTools.generateToken()
                if generateFiles(token, size):
                    return token
                else:
                    return "Error : Unable to create the necessary files."
            else:
                return "Error : Missing or too much data."
        else:
            return "Error : Data type not respected."
    else:
        return "Error : Missing argument(s)."


def DataReceivedProcessor(token, packetNb, data):
    try:
        with open("../output/temp/" + token + ".temp", "a") as tempFile:
            tempFile.write(packetNb + "|" + data + "\n")
        return True
    except:
        return False


def UploadHandler(parameters):
    if len(parameters) >= 3:
        if GlobalTools.checkToken(parameters[0]):
            if parameters[1].isdigit():
                if DataReceivedProcessor(parameters[0], parameters[1], parameters[2]):
                    return "OK"
                else:
                    return "Error : Unable to process packet."
            else:
                return "Error : Invalid packet number."
        else:
            return "Error : Invalid token."
    else:
        return "Error : Missing argument(s)."


def TemporaryDataProcessor(token):
    try:
        tempFileData = list(OrderedDict.fromkeys(open("../output/temp/" + token + ".temp","r").readlines()))
        tempFileData.sort(key=lambda packet:int(packet.split("|")[0]))
        
        outputData = json.loads(open("../output/json/" + token + ".json","r").read())
        
        for packet in tempFileData:
            packetData = ((packet.split("|")[1]).rstrip()).split(",")
            for singleBlock in packetData:
                outputData["blocks"].append(singleBlock)
            
        outputFile = open("../output/json/" + token + ".json", "w")
        outputFile.write(json.dumps(outputData))
        outputFile.close()
        
        os.remove("../output/temp/" + token + ".temp")
        
        return True
    except:
        return False


def EndHandler(parameters):
    if len(parameters) >= 1:
        if GlobalTools.checkToken(parameters[0]):
            if TemporaryDataProcessor(parameters[0]):
                return "OK"
            else:
                return "Error : Unable to process received blocks data."
        else:
            return "Error : Invalid token."
    else:
        return "Error : Missing argument(s)."


def LTJManager(parsedURLArgs):
    if len(parsedURLArgs) >= 1:
        if parsedURLArgs[0] == "new":
            return NewSchematicHandler(parsedURLArgs[1:])
        elif parsedURLArgs[0] == "ul":
            return UploadHandler(parsedURLArgs[1:])
        elif parsedURLArgs[0] == "end":
            return EndHandler(parsedURLArgs[1:])
        elif parsedURLArgs[0] == "getMaxSize":
            return maxSize
        else:
            return "Error : Invalid argument(s)."
    else:
        return "Error : Missing argument(s)."