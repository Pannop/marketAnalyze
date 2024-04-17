import eel
from marketAnalyzer import MarketMatrix

eel.init("./src/web/")

winSize = None
marketMatrix = None



def __init__(dimX, dimY, marketMatrixObj: MarketMatrix):
    global winSize
    winSize = [dimX, dimY]
    global marketMatrix
    marketMatrix = marketMatrixObj

def start():
    marketMatrix.loadCache()
    marketMatrix.loadData()
    marketMatrix.saveCache()
    eel.start("start.html", size=winSize)

@eel.expose
def setDefaultSize():
    eel.setSize(winSize[0], winSize[1])

@eel.expose
def loadData():
    eel.setData(marketMatrix.cache)

@eel.expose
def formatData(markets, fromDate, toDate, interval):
    if(len(markets)==0):
        return []
    data = marketMatrix.getMarketsData(markets, fromDate, toDate, interval)
    formattedData = []
    for t in range(len(data[markets[0]])):
        formattedData.append([t])
        for m in markets:
            formattedData[t].append(data[m][t]["value"])
    eel.applyMarketChart(formattedData) 

    

