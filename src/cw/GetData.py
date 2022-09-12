import requests
import json
from configparser import ConfigParser
import csv_conversion
import os
from src.gns import GNS
import time

config = ConfigParser()
config.read(r'C:\Users\rubxu\Desktop\recruitment-2022-python-ReubenXuereb-main\config\config.ini')
roc = config.get('general', 'rate_of_change')
floatROC = float(roc)
tps = config.get('general', 'time_period_seconds')
floatTPS = float(tps)
cc = config.get('general', 'cryptocurrencies')
currencyList = cc.split(',')
fiat_ = config.get('general', 'fiat')
fiatList = fiat_.split(',')


combinedList = []
# for loop that combines currencies with fiats from the config.ini file
def Pairs():
    for currency in currencyList:
        for symbol in fiatList:
            combination = currency + symbol
            combinedList.append(combination)



#Runs the script
def RunMethod():
    startTime = time.time()
    while True:
        print("----------------------------------------------")
        print("Started")
        API()
        time.sleep(floatTPS - ((time.time() - startTime) % floatTPS))


#checks if file exits or not.
def API():
    filename = "Prices.csv"
    if os.path.exists(filename):
        os.remove("Prices.csv")
    GetPrices()


#method that sends the request to the api and gets price, coin and fiat.
priceList = []
def GetPrices():
    url_price = "https://api.cryptowat.ch/markets/kraken/"
    url_pair = "https://api.cryptowat.ch/pairs/"
    priceString = "/price"
    if not priceList:
        for ticker in combinedList:
            currentCurrency = ticker
            apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
            apiUrlPair = requests.get(url_pair + currentCurrency)
            loadUrlPrice = json.loads(apiUrlPrice.text)
            loadUrlPair = json.loads(apiUrlPair.text)
            price = loadUrlPrice.get('result').get('price')
            coin = loadUrlPair.get('result').get('base').get('symbol')
            fiat = loadUrlPair.get('result').get('quote').get('symbol')
            print(currentCurrency, "price is:", price)
            priceList.append(price)
            csv_conversion.CsvFile(price, coin, fiat)
    else:
        for ticker in combinedList:
            currentCurrency = ticker
            apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
            apiUrlPair = requests.get(url_pair + currentCurrency)
            loadUrlPrice = json.loads(apiUrlPrice.text)
            loadUrlPair = json.loads(apiUrlPair.text)
            price = loadUrlPrice.get('result').get('price')
            coin = loadUrlPair.get('result').get('base').get('symbol')
            fiat = loadUrlPair.get('result').get('quote').get('symbol')
            print(currentCurrency, "price is:", price)
            priceList.append(price)
            ComparePrices(currentCurrency)
            csv_conversion.CsvFile(price, coin, fiat)


#method that compares current currencies's prices, gets the rate of change and compares with config.ini rate of change
def ComparePrices(currentCurrency):
    countPriceList = len(priceList)
    if countPriceList < 24:
        prevPriceIndex = countPriceList - 7
        prevPrice = priceList[prevPriceIndex]
        newPrice = priceList[-1]
        print(currentCurrency, "'s Previous Price: ", prevPrice)
        print(currentCurrency, "'s Newest Price: ", newPrice)
        rateOfChange = (newPrice - prevPrice) / prevPrice
        print("Rate of Change of", currentCurrency, "is: ", rateOfChange)
        if prevPrice == newPrice:
            print("Rate stayed the same")
            print("-------------------")
        elif rateOfChange > floatROC:
            GNS.send_to_gns("Rate Increased")
            print("-------------------")
        elif rateOfChange < floatROC:
            GNS.send_to_gns("Rate Decreased")
            print("-------------------")

    elif countPriceList >= 24:
        prevPriceIndex = countPriceList - 7
        prevPrice = priceList[prevPriceIndex]
        newPrice = priceList[-1]
        print(currentCurrency, "'s Previous Price: ", prevPrice)
        print(currentCurrency, "'s Newest Price: ", newPrice)
        rateOfChange = (newPrice - prevPrice) / prevPrice
        print("Rate of Change of", currentCurrency, "is: ", rateOfChange)
        if prevPrice == newPrice:
            print("Rate stayed the same")
            print("-------------------")
        elif rateOfChange > floatROC:
            GNS.send_to_gns("Rate Increased")
            print("-------------------")
        elif rateOfChange < floatROC:
            GNS.send_to_gns("Rate Decreased")
            print("-------------------")
        #Delete first 12 elements in list
        del priceList[:12]

Pairs()
RunMethod()
