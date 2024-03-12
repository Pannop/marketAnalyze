import requests
import pandas
import json
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


jsonToXlsx(getBIMarketData("DE000VU32806"))
jsonToXlsx(calculateDelta(getBIMarketData("DE000VU32806")), "jsonDeltaFile.json", "excelDeltaFile.xlsx")

#print(getUSMarketData("TIME_SERIES_DAILY", "IBM", "outputsize=full"))
