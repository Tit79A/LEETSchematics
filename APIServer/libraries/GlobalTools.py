import os
import binascii


def makeNeededDirectories():
    os.makedirs("../output", exist_ok=True)
    os.makedirs("../output/json", exist_ok=True)
    os.makedirs("../output/temp", exist_ok=True)
    os.makedirs("../output/schematic", exist_ok=True)


def canStringArrayBePositiveIntArray(stringArray):
    result = True
    
    for element in range (0, len(stringArray)):
        if not stringArray[element].isdigit():
            result = False
    
    return result


def generateToken():
    token = binascii.hexlify(os.urandom(3)).decode()
    while checkToken(token):
        token = binascii.hexlify(os.urandom(3)).decode()
    return token


def checkToken(token):
    return (os.path.exists("../output/json/" + token + ".json")
        or os.path.exists("../output/schematic/" + token + ".schematic"))