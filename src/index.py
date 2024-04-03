import datetime
import os
import requests
import pandas
import json
import numpy as np
import time
import math
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


def getYaMarketData(symbol,interval="1d"):
    t = str(time.time()).split(".")[0]
    header = {
    "Host": "query1.finance.yahoo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",    "Upgrade-Insecure-Requests": "1",
    "Cookie": "A3=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY; A1=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY; GUC=AQAACAFl8e1mIkIfJgSt&s=AQAAAFcXkJ1O&g=ZfCm1w; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiUFNESzVNTjRYN0xWRjVVMzJTR1AzNTVDV1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiIxZXBNbkMyMWhmbjkifX0.uVZ1PMsWmbl8EBrsCYaDa1xpFQdlInXecdyUqAPaQNSxro9447GvRX97Yonc7Dk2usPwT8ygXpQuQhDiYl8Tj0Fu5OCNuo_JoVEoyfV7GrlYm3-yM2oxWjicO53qWfPHeE050D2H4AfFw_lASAagpoHuN2eTlEj7SG14EL2mMpU; T=af=JnRzPTE3MTAyNzAxNDMmcHM9MzZyNnBoSmhoXzUwRFN0aWdJQlVtUS0t&d=bnMBeWFob28BZwFQU0RLNU1ONFg3TFZGNVUzMlNHUDM1NUNXWQFhYwFBTVlSdDZGcgFhbAFhbmRlcmxpbmlsZW9uYXJkbzIwMjBAZ21haWwuY29tAXNjAW1icl9sb2dpbgFmcwFIZzZyanJCbDhLYW8BenoBL2FLOGxCQTdFAWEBUUFFAWxhdAEvYUs4bEIBbnUBMA--&kt=EAAsGitdcakPGbY7irhMab_UQ--~I&ku=FAAorceeKNG.dFwPvHECfavzXuPQWkdaBpQrGQlQKgb8SimM0JGDaieeHi_4t1nV.fzzq4dXhPHXjZ9b6mlU7ApxAA.EAq.SjisF.ObYlJilkAQ24C9eFlOj8CRU2q8ldx_LzyVSK26Rvg8VTg1GC7oynUiGXYYlAbBZO5rxS_xYyE-~E; F=d=GzmZX_s9vJVWdy9AtP9WyR.sUT1t94C_KyfMZQucvctigjhhRz0cVK51Ud2PxXG1vMy7; PH=l=it-IT; Y=v=1&n=5sggjh94ph61e&l=ix0gc8w961a6944l5hmwm6n5uhk3m0bke9pgsmhn/o&p=n38vvit00000000&r=1d5&intl=it; cmp=t=1711488666&j=1&u=1---&v=19; PRF=t%3DFTSEMIB.MI%252BAAPL%26newChartbetateaser%3D0%252C1711488327445; A1S=d=AQABBGsrHGUCEJLfk6jwialcr4U1OUFzQUYFEgAACAHt8WUiZudVb2UB9qMAAAcIayscZUFzQUYID5vc8d2S8mYEiBe6cprBswkBBwoB3Q&S=AQAAAs5BXlimiiyRnEt7kF0KkjY",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "domain-id": "it"}
    req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1=0&period2={t}&useYfid=true&interval={interval}&includePrePost=true&events=div|split|earn&lang=it-IT&region=IT&crumb=bZtbC8282C3&corsDomain=it.finance.yahoo.com", headers=header)
    return req.json()

def calculateBIDelta(data, fromYear=0, dayStep=1):
    deltas = []
    for i in range(dayStep, len(data), dayStep):
        if(int(data[i]["time"][:4])>=fromYear):
            deltas.append({"time":data[i]["time"], "deltaPerc":round((data[i]["price"]-data[i-dayStep]["price"])/data[i-dayStep]["price"], 7),"delta":(data[i]["price"]-data[i-dayStep]["price"]), "value":data[i]["price"]})
    return deltas

def calculateYaDelta(data, fromYear=0, dayStep=1):
    deltas = []
    x=data["chart"]["result"][0]["timestamp"]

    y=data["chart"]["result"][0]["indicators"]["quote"][0]
    for i in range(dayStep, len(x), dayStep):
        if(x[i] and y["close"][i] and x[i-dayStep] and y["close"][i-dayStep] and int(str(datetime.date.fromtimestamp(x[i]))[:4])>=fromYear):
            deltas.append({"time":str(datetime.date.fromtimestamp(x[i])), "deltaPerc":round((y["close"][i]-y["close"][i-dayStep])/y["close"][i-dayStep], 7),"delta":(y["close"][i]-y["close"][i-dayStep]), "value":y["close"][i]})
    return deltas


DATA_DIR = "./data/"
def jsonToXlsx(data, jsonFile="jsonFile.json", excelFile="excelFile.xlsx"):
    with open(DATA_DIR+jsonFile, "w") as file:
        file.write(json.dumps(data))
    dataPd = pandas.read_json(DATA_DIR+jsonFile)
    return dataPd.to_excel(DATA_DIR+excelFile)

def summt(d0, a0, d1, a1):
        s=0
        for i in range(len(d0)):
            s+=(d0[i]-a0)*(d1[i]-a1)
        return s

class MarketMatrix:

    def __init__(self, marketList, indexName):
        self.marketList = marketList
        #mat = [[0.]*len(marketList)]*len(marketList)
        #mat = [[0.]*len(marketList) for n in range(len(marketList))]
        #lst = [0.]*len(marketList)
        self.correlationMarketMatrix = np.array([[0.]*len(marketList) for n in range(len(marketList))])
        self.betaMarketMatrix = np.array([[0.]*len(marketList) for n in range(len(marketList))])
        self.correlationIndexList = np.array([0.]*len(marketList))
        self.betaIndexList = np.array([0.]*len(marketList))
        self.marketData = {}
        self.indexData = {}
        self.corrispondences=[]
        self.indexName = indexName
        self.CORRISPONDECE_THRESHOLD = 0.6

        
    def loadMarketData(self, fromYear=0, dayStep=1):
        for m in self.marketList:
            print(f'getting {m}')
            self.marketData[m] = {}
            self.marketData[m]["d"] = calculateYaDelta(getYaMarketData(m, "1d"), fromYear, dayStep)
            self.marketData[m]["wk"] = calculateYaDelta(getYaMarketData(m, "1wk"), fromYear, dayStep)


    def loadIndexData(self, fromYear=0, dayStep=1):
        self.indexData["d"] = calculateYaDelta(getYaMarketData(self.indexName, "1d"), fromYear, dayStep)
        self.indexData["wk"] = calculateYaDelta(getYaMarketData(self.indexName, "1wk"), fromYear, dayStep)

            
    def calculateMarketCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(m1!=m0):
                    if(len(self.marketData[m0Name]["d"]) > 0 and len(self.marketData[m1Name]["d"]) > 0):
                        m0Times = [v["time"] for v in self.marketData[m0Name]["d"]]
                        m1Times = [v["time"] for v in self.marketData[m1Name]["d"]]
                        commonTimes = [v for v in m1Times if v in m0Times]
                        self.correlationMarketMatrix[m0][m1] = self.calculateCorrelation([v["value"] for v in self.marketData[m0Name]["d"] if v["time"] in commonTimes], [v["value"] for v in self.marketData[m1Name]["d"] if v["time"] in commonTimes])
                    else:
                        self.correlationMarketMatrix[m0][m1] = 0
                else:
                    self.correlationMarketMatrix[m0][m1] = 1
    
    def calculateMarketBetas(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(len(self.marketData[m0Name]["wk"]) > 0 and len(self.marketData[m1Name]["wk"]) > 0):
                    m0Times = [v["time"] for v in self.marketData[m0Name]["wk"]]
                    m1Times = [v["time"] for v in self.marketData[m1Name]["wk"]]
                    commonTimes = [v for v in m1Times if v in m0Times]
                    self.betaMarketMatrix[m0][m1] = self.calculateBeta([v["deltaPerc"] for v in self.marketData[m0Name]["wk"] if v["time"] in commonTimes], [v["deltaPerc"] for v in self.marketData[m1Name]["wk"] if v["time"] in commonTimes])
                else:
                    self.betaMarketMatrix[m0][m1] = 0


    def calculateIndexCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            if(len(self.marketData[m0Name]["d"]) > 0):    
                m0Times = [v["time"] for v in self.marketData[m0Name]["d"]]
                indxTimes = [v["time"] for v in self.indexData["d"]]
                commonTimes = [v for v in indxTimes if v in m0Times]
                self.correlationIndexList[m0] = self.calculateCorrelation([v["value"] for v in self.marketData[m0Name]["d"] if v["time"] in commonTimes], [v["value"] for v in self.indexData["d"] if v["time"] in commonTimes])
            else:
                self.correlationIndexList[m0] = -2

    


    def calculateCorrelation(self, data0, data1):
        av0 = sum(data0)/len(data0)
        av1 = sum(data1)/len(data1)
        return summt(data0, av0, data1, av1) / math.sqrt(summt(data0, av0, data0, av0)*summt(data1, av1, data1, av1))
        


    def calculateBeta(self, data0, data1):
        av0 = sum(data0)/len(data0)
        av1 = sum(data1)/len(data1)
        return summt(data0, av0, data1, av1) / summt(data1, av1, data1, av1)


    
    def calculateIndexBetas(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            if(len(self.marketData[m0Name]["wk"]) > 0):
                m0Times = [v["time"] for v in self.marketData[m0Name]["wk"]]
                indxTimes = [v["time"] for v in self.indexData["wk"]]
                commonTimes = [v for v in indxTimes if v in m0Times]
                self.betaIndexList[m0] = self.calculateBeta([v["deltaPerc"] for v in self.marketData[m0Name]["wk"] if v["time"] in commonTimes], [v["deltaPerc"] for v in self.indexData["wk"] if v["time"] in commonTimes])
            else:
                self.betaIndexList[m0] = 0



    def createCorrispondences(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(m0!=m1):
                    if(self.correlationMarketMatrix[m0][m1]>self.CORRISPONDECE_THRESHOLD or self.correlationMarketMatrix[m0][m1]<-self.CORRISPONDECE_THRESHOLD):
                        self.corrispondences.append({"title1":m0Name, "title2":m1Name, "correlation":self.correlationMarketMatrix[m0][m1], "beta":self.betaMarketMatrix[m0][m1]})
                    elif(self.correlationIndexList[m0]>self.CORRISPONDECE_THRESHOLD or self.correlationIndexList[m0]<-self.CORRISPONDECE_THRESHOLD):
                        self.corrispondences.append({"title1":m0Name, "title2":self.indexName, "correlation":self.correlationIndexList[m0], "beta":self.betaIndexList[m0]})
  

    def loadData(self, fromYear=0, dayStep=1):
        self.loadMarketData(fromYear,dayStep)
        self.loadIndexData(fromYear,dayStep)
        self.calculateMarketCorrelation()
        self.calculateMarketBetas()
        self.calculateIndexCorrelation()
        self.calculateIndexBetas()
        self.createCorrispondences()                  
            
        
        



#jsonToXlsx(getBIMarketData("DE000VU32806"))
#jsonToXlsx(calculateDelta(getBIMarketData("DE000VU32806")), "jsonDeltaFile.json", "excelDeltaFile.xlsx")
#print(getUSMarketData("TIME_SERIES_DAILY", "IBM", "outputsize=full"))
    
MARKET_NUM = 5
FROM_YEAR = 2019
DAY_STEP = 1


fileIn = open("resources/marketListCode.txt", "r")
l = fileIn.read().split("\n")
fileIn.close()
mm = MarketMatrix(l[:MARKET_NUM], "FTSEMIB.MI")
mm.loadData(FROM_YEAR, DAY_STEP)
jsonToXlsx(mm.indexData["d"], excelFile="indexDataDalily.xlsx")
jsonToXlsx(mm.marketData["AZM.MI"]["d"], excelFile="azimutDataDaily.xlsx")
jsonToXlsx(mm.indexData["wk"], excelFile="indexDataWeekly.xlsx")
jsonToXlsx(mm.marketData["AZM.MI"]["wk"], excelFile="azimutDataWeekly.xlsx")
jsonToXlsx(mm.corrispondences, excelFile="validTitles.xlsx")

print("correlations: ", mm.correlationIndexList)
print("betas: ",mm.betaIndexList)
print("valid: ", mm.corrispondences)

fileOut = open("data/matrix.txt", "w")
fileOut.write("coef corr\n")
fileOut.write(str(mm.correlationMarketMatrix))
fileOut.write("\n\nbetas\n")
fileOut.write(str(mm.betaMarketMatrix))
jsonToXlsx([mm.marketList] + mm.correlationMarketMatrix.tolist(), excelFile="correlation.xlsx")
jsonToXlsx([mm.marketList] + mm.betaMarketMatrix.tolist(), excelFile="beta.xlsx")
fileOut.close()
