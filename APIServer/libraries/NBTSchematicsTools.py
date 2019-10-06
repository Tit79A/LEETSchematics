import os
import json
from nbtschematic import SchematicFile


def generateSchematicFromBlocksFile(inputFile,outputDirectory):
    if os.path.isfile(inputFile):
        if os.path.exists(outputDirectory) and (not os.path.isfile(outputDirectory)):
            inputData = json.loads(open(inputFile,"r").read())
            
            schematic = SchematicFile(shape=(inputData["height"], inputData["length"], inputData["width"]))
            assert schematic.blocks.shape == (inputData["height"], inputData["length"], inputData["width"])
            
            currentBlock = 0
            for x in range (0, inputData["width"]):
                for y in range (0, inputData["height"]):
                    for z in range (0, inputData["length"]):
                        schematic.blocks[y,z,x] = int((inputData["blocks"][currentBlock]).split(":")[0])
                        schematic.data[y,z,x] = int((inputData["blocks"][currentBlock]).split(":")[1])
                        currentBlock += 1
            
            schematic.save(outputDirectory + "/" + os.path.splitext(os.path.basename(inputFile))[0] + ".schematic")
            
            return "Success : Schematic file saved to : " + outputDirectory + "/" + os.path.splitext(os.path.basename(inputFile))[0] + ".schematic !"
        else:
            return "Error : Output specified doesn't exist or is not a directory."
    else:
        return "Error : Input file doesn't exist."


def readBlocksFromSchematicFile(inputFile,outputDirectory):
    if os.path.isfile(inputFile):
        if os.path.exists(outputDirectory) and (not os.path.isfile(outputDirectory)):
            schematic = SchematicFile.load(inputFile)
            
            outputData = {}
            outputData["width"], outputData["height"], outputData["length"] = schematic.blocks.shape
            outputData["blocks"] = []
            
            for x in range (0, outputData["width"]):
                for y in range (0, outputData["height"]):
                    for z in range (0, outputData["length"]):
                        outputData["blocks"].append(str(int(schematic.blocks[x,y,z])) + ":" + str(int(schematic.data[x,y,z])))
            
            outputFile = open(outputDirectory + "/" + os.path.splitext(os.path.basename(inputFile))[0] + ".json", "w")
            outputFile.write(json.dumps(outputData))
            outputFile.close()
            
            return "Success : Blocks file saved to : " + outputDirectory + "/" + os.path.splitext(os.path.basename(inputFile))[0] + ".json !"
        else:
            return "Error : Output specified doesn't exist or is not a directory."
    else:
        return "Error : Input file doesn't exist."