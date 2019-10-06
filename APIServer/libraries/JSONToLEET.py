from libraries import GlobalTools


def JTLManager(parsedURLArgs):
    if len(parsedURLArgs) >= 1:
        if GlobalTools.checkToken(parsedURLArgs[0]):
            return open("../output/json/" + parsedURLArgs[0] + ".json","r").read()