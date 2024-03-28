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


def getYaMarketData(symbol):
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
    req = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1=0&period2={t}&useYfid=true&interval=1d&includePrePost=true&events=div|split|earn&lang=it-IT&region=IT&crumb=bZtbC8282C3&corsDomain=it.finance.yahoo.com", headers=header)
    return req.json()

def calculateBIDelta(data, fromYear=0):
    deltas = []
    for i in range(1, len(data)):
        if(int(data[i]["time"][:4])>=fromYear):
            deltas.append({"time":data[i]["time"], "deltaPerc":round((data[i]["price"]-data[i-1]["price"])*100/data[i-1]["price"], 7),"delta":(data[i]["price"]-data[i-1]["price"]), "value":data[i]["price"]})
    return deltas

def calculateYaDelta(data, fromYear=0):
    deltas = []
    x=data["chart"]["result"][0]["timestamp"]

    y=data["chart"]["result"][0]["indicators"]["quote"][0]
    for i in range(1, len(x)):
        if(x[i] and y["open"][i] and int(str(datetime.date.fromtimestamp(x[i]))[:4])>=fromYear):
            deltas.append({"time":str(datetime.date.fromtimestamp(x[i])), "deltaPerc":round((y["close"][i]-y["open"][i])*100/y["open"][i], 7),"delta":(y["close"][i]-y["open"][i]), "value":y["close"][i]})
    return deltas


DATA_DIR = "./data/"
def jsonToXlsx(data, jsonFile="jsonFile.json", excelFile="excelFile.xlsx"):
    with open(DATA_DIR+jsonFile, "w") as file:
        file.write(json.dumps(data))
    dataPd = pandas.read_json(DATA_DIR+jsonFile)
    return dataPd.to_excel(DATA_DIR+excelFile)


class MarketMatrix:

    def __init__(self, marketList, indexName):
        self.marketList = marketList
        mat = [[0.]*len(marketList)]*len(marketList)
        lst = [0.]*len(marketList)
        self.correlationMarketMatrix = np.array(mat)
        self.betaMarketMatrix = np.array(mat)
        self.correlationIndexList = np.array(lst)
        self.betaIndexList = np.array(lst)
        self.marketData = {}
        self.indexData = []
        self.corrispondences=[]
        self.indexName = indexName
        self.CORRISPONDECE_THRESHOLD = 0.6

        
    def loadMarketData(self, fromYear=0):
        for m in self.marketList:
            self.marketData[m] = calculateBIDelta(getBIMarketData(m), fromYear)
            print(f'getting {m}, l: {len(self.marketData[m])}')

    def loadIndexData(self, fromYear=0):
        self.indexData = calculateYaDelta(getYaMarketData(self.indexName))

            
    def calculateMarketCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            for m1 in range(marketNum):
                m1Name = self.marketList[m1]
                if(m1!=m0):
                    if(len(self.marketData[m0Name]) > 0 and len(self.marketData[m1Name]) > 0):
                        dataLen = min(len(self.marketData[m0Name]), len(self.marketData[m1Name]))
                
                        self.correlationMarketMatrix[m0][m1] = round(np.corrcoef([np.array([v["value"] for v in self.marketData[m0Name][-dataLen:]]), np.array([v["value"] for v in self.marketData[m1Name][-dataLen:]])])[0][1], 3)
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
                if(len(self.marketData[m0Name]) > 0 and len(self.marketData[m1Name]) > 0):
                    dataLen = min(len(self.marketData[m0Name]), len(self.marketData[m1Name]))
                    self.betaMarketMatrix[m0][m1] = round(np.cov([np.array([v["deltaPerc"] for v in self.marketData[m0Name][-dataLen:]]), np.array([v["deltaPerc"] for v in self.marketData[m1Name][-dataLen:]])])[0][1]/np.cov([np.array([v["deltaPerc"] for v in self.marketData[m1Name][-dataLen:]]), np.array([v["deltaPerc"] for v in self.marketData[m1Name][-dataLen:]])])[0][1], 3)
                else:
                    self.betaMarketMatrix[m0][m1] = 0


    def calculateIndexCorrelation(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            if(len(self.marketData[m0Name]) > 0):
                dataLen = min(len(self.marketData[m0Name]), len(self.indexData))
    
                self.correlationIndexList[m0] = round(np.corrcoef([np.array([v["value"] for v in self.marketData[m0Name][-dataLen:]]), np.array([v["value"] for v in self.indexData[-dataLen:]])])[0][1], 3)
            else:
                self.correlationIndexList[m0] = -2


    def calulateBeta(self, data0, data1):
        s1 = 0
        c=0
        for d in data0:
            if(d!=0):
                c+=1
                s1+=d
        avg0 = s1/c
        avg1 = sum(data1)/len(data1)
        print("index",avg0)
        print("title",avg1)


    
    def calculateIndexBetas(self):
        marketNum = len(self.marketList)
        for m0 in range(marketNum):
            m0Name = self.marketList[m0]
            if(len(self.marketData[m0Name]) > 0):
                dataLen = min(len(self.marketData[m0Name]), len(self.indexData))
                mat = np.cov([np.array([v["deltaPerc"] for v in self.indexData[-dataLen:]]), np.array([v["deltaPerc"] for v in self.marketData[m0Name][-dataLen:]])])
                den = np.cov([np.array([v["deltaPerc"] for v in self.indexData[-dataLen:]]), np.array([v["deltaPerc"] for v in self.indexData[-dataLen:]])])[0][0]
                print(mat[0][0]/den)
                print(mat[0][1]/den)
                print(mat[1][1]/den)
                print(self.calulateBeta([v["deltaPerc"] for v in self.indexData], [v["deltaPerc"] for v in self.marketData[m0Name][-dataLen:]]))
                print("-------------------------------------")
                self.betaIndexList[m0] = round(np.cov([np.array([v["deltaPerc"] for v in self.indexData[-dataLen:]]), np.array([v["deltaPerc"] for v in self.marketData[m0Name][-dataLen:]])])[0][1]/np.cov([np.array([v["deltaPerc"] for v in self.indexData[-dataLen:]]), np.array([v["deltaPerc"] for v in self.indexData[-dataLen:]])])[0][1], 3)
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
  

    def loadData(self, fromYear=0):
        self.loadMarketData(fromYear)
        self.loadIndexData()
        self.calculateMarketCorrelation()
        self.calculateMarketBetas()
        self.calculateIndexCorrelation()
        self.calculateIndexBetas()
        self.createCorrispondences()                  
            
        
        



#jsonToXlsx(getBIMarketData("DE000VU32806"))
#jsonToXlsx(calculateDelta(getBIMarketData("DE000VU32806")), "jsonDeltaFile.json", "excelDeltaFile.xlsx")
#print(getUSMarketData("TIME_SERIES_DAILY", "IBM", "outputsize=full"))
    
MARKET_NUM = 5
FROM_YEAR = 0


fileIn = open("resources/marketList.txt", "r")
l = fileIn.read().split("\n")
fileIn.close()
mm = MarketMatrix(l[:MARKET_NUM], "FTSEMIB.MI")
mm.loadData(FROM_YEAR)
jsonToXlsx(mm.indexData, excelFile="indexData.xlsx")

print(mm.betaIndexList)

fileOut = open("data/matrix.txt", "w")
fileOut.write("coef corr\n")
fileOut.write(str(mm.correlationMarketMatrix))
fileOut.write("\n\nbetas\n")
fileOut.write(str(mm.betaMarketMatrix))
jsonToXlsx([mm.marketList] + mm.correlationMarketMatrix.tolist(), excelFile="correlation.xlsx")
jsonToXlsx([mm.marketList] + mm.betaMarketMatrix.tolist(), excelFile="beta.xlsx")
fileOut.close()
