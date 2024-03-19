import requests
import pandas
import json
import numpy as np
AV_KEY = "NPRZ3R6XPBJWSA26"


def getUSMarketData(func, symbol, additional):
    req = requests.get(f'https://www.alphavantage.co/query?function={func}&symbol={symbol}&apikey={AV_KEY}&{additional}')
    return req.json()

def getBIMarketData(symbol):
    req = requests.get(f"https://live.euronext.com/en/instrumentSearch/searchJSON?q={symbol}")
    response = req.json()
    if(len(response)==1):
        isin = symbol
        mic = "SEDX"
    else:
        isin = response[0]["isin"]
        mic = response[0]["mic"]
    req = requests.get(f"https://live.euronext.com/intraday_chart/getChartData/{isin}-{mic}/max")
    return req.json()

def calculateDelta(data):
    deltas = []
    for i in range(1, len(data)):
        deltas.append({"time":data[i]["time"], "delta":round((data[i]["price"]-data[i-1]["price"])/data[i-1]["price"], 7)})
    return deltas


DATA_DIR = "./data/"
def jsonToXlsx(data, jsonFile="jsonFile.json", excelFile="excelFile.xlsx"):
    with open(DATA_DIR+jsonFile, "w") as file:
        file.write(json.dumps(data))
    dataPd = pandas.read_json(DATA_DIR+jsonFile)
    return dataPd.to_excel(DATA_DIR+excelFile)


class MarketMatrix:
    def __init__(self, marketList):
        self.marketList = marketList
        mat = [[0.]*len(marketList)]*len(marketList)
        self.correlationMatrix = np.array(mat)
        self.betaMatrix = np.array(mat)
        self.marketData = {}
        
    def loadMarketData(self):
        for m in self.marketList:
            self.marketData[m] = calculateDelta(getBIMarketData(m))
            print(f'getting {m}, l: {len(self.marketData[m])}')
            
    def calculateCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(m1!=m0):
                    if(len(self.marketData[m0Name]) > 0 and len(self.marketData[m1Name]) > 0):
                        dataLen = min(len(self.marketData[m0Name]), len(self.marketData[m1Name]))
                
                        self.correlationMatrix[m0][m1] = round(np.corrcoef([np.array([v["delta"] for v in self.marketData[m0Name][-dataLen:]]), np.array([v["delta"] for v in self.marketData[m1Name][-dataLen:]])])[0][1], 3)
                    else:
                        self.correlationMatrix[m0][m1] = -2
                else:
                    self.correlationMatrix[m0][m1] = 1
    
    def calculateBetas(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(len(self.marketData[m0Name]) > 0 and len(self.marketData[m1Name]) > 0):
                    dataLen = min(len(self.marketData[m0Name]), len(self.marketData[m1Name]))
                    print(np.var( np.array([v["delta"] for v in self.marketData[m1Name][-dataLen:]])))
                    self.betaMatrix[m0][m1] = round(np.cov([np.array([v["delta"] for v in self.marketData[m0Name][-dataLen:]]), np.array([v["delta"] for v in self.marketData[m1Name][-dataLen:]])])[0][1]/np.cov([np.array([v["delta"] for v in self.marketData[m1Name][-dataLen:]]), np.array([v["delta"] for v in self.marketData[m1Name][-dataLen:]])])[0][1], 3)
                else:
                    self.betaMatrix[m0][m1] = -2

        pass
        



#jsonToXlsx(getBIMarketData("DE000VU32806"))
#jsonToXlsx(calculateDelta(getBIMarketData("DE000VU32806")), "jsonDeltaFile.json", "excelDeltaFile.xlsx")
#print(getUSMarketData("TIME_SERIES_DAILY", "IBM", "outputsize=full"))
    
MARKET_NUM = 5

fileIn = open("resources/marketList.txt", "r")
l = fileIn.read().split("\n")
fileIn.close()
mm = MarketMatrix(l[:MARKET_NUM])
mm.loadMarketData()
mm.calculateCorrelation()
mm.calculateBetas()
fileOut = open("data/matrix.txt", "w")
fileOut.write("coef corr\n")
fileOut.write(str(mm.correlationMatrix))
fileOut.write("\n\nbetas\n")
fileOut.write(str(mm.betaMatrix))
jsonToXlsx([mm.marketList] + mm.correlationMatrix.tolist(), excelFile="correlation.xlsx")
jsonToXlsx([mm.marketList] + mm.betaMatrix.tolist(), excelFile="beta.xlsx")
fileOut.close()
