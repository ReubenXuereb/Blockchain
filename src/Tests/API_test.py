import requests
import json
from configparser import ConfigParser
import src.cw.csv_conversion as csv_conversion
import os
from src.gns import GNS
import time


# response_btc_API = requests.get("https://api.cryptowat.ch/markets/kraken/btceur/price")
# print(response_API.status_code)
# print(response_btc_API.json())
# data = json.loads(response_btc_API.text)
# print(data)



config = ConfigParser()
config.read(r'C:\Users\rubxu\Desktop\recruitment-2022-python-ReubenXuereb-main\config\config.ini')
# print(config.sections())
roc = config.get('general', 'rate_of_change')
floatROC = float(roc)
tps = config.get('general', 'time_period_seconds')
floatTPS = float(tps)
# print(floatROC, floatTPS)
cc = config.get('general', 'cryptocurrencies')
currencyList = cc.split(',')
# print(currency_list)
fiat_ = config.get('general', 'fiat')
fiatList = fiat_.split(',')
# print(fiat_list)



combinedList = []

# for loop that combines currencies with fiats from the config.ini file
def Pairs():
    for currency in currencyList:
        for symbol in fiatList:
            combination = currency + symbol
            print(combination)
            combinedList.append(combination)


# print("Combination list: ", combined_list)

def RunMethod():
    startTime = time.time()
    while True:
        print("Timer Started!")
        API()
        time.sleep(floatTPS - ((time.time() - startTime) % floatTPS))




def API():
    filename = "../cw/Prices.csv"
    if os.path.exists(filename):
        os.remove("../cw/Prices.csv")
        print("thalt hawn ghax il file ga jezisti")
    #Pairs()
    GetPrices2()



priceList = []

def GetPrices2():
    url_price = "https://api.cryptowat.ch/markets/kraken/"
    url_pair = "https://api.cryptowat.ch/pairs/"
    priceString = "/price"
    if not priceList:
        for ticker in combinedList:
            print("Thalt l ewwel darba.")
            currentCurrency = ticker
            apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
            apiUrlPair = requests.get(url_pair + currentCurrency)
            print(currentCurrency, ":", apiUrlPrice.json())
            # print(currentCurrency, ':', apiUrlPair.json())
            loadUrlPrice = json.loads(apiUrlPrice.text)
            loadUrlPair = json.loads(apiUrlPair.text)
            price = loadUrlPrice.get('result').get('price')
            coin = loadUrlPair.get('result').get('base').get('symbol')
            fiat = loadUrlPair.get('result').get('quote').get('symbol')
            # print(coin, fiat)
            print(currentCurrency, "price is:", price)
            priceList.append(price)
            print("Prev Prices: ", priceList)
            csv_conversion.CsvFile(price, coin, fiat)
    else:
        for ticker in combinedList:
            print("Thalt it tieni darba.")
            currentCurrency = ticker
            apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
            apiUrlPair = requests.get(url_pair + currentCurrency)
            print(currentCurrency, ":", apiUrlPrice.json())
            # print(currentCurrency, ':', apiUrlPair.json())
            loadUrlPrice = json.loads(apiUrlPrice.text)
            loadUrlPair = json.loads(apiUrlPair.text)
            price = loadUrlPrice.get('result').get('price')
            coin = loadUrlPair.get('result').get('base').get('symbol')
            fiat = loadUrlPair.get('result').get('quote').get('symbol')
            # print(coin, fiat)
            print(currentCurrency, "price is:", price)
            priceList.append(price)
            print("New Prices: ", priceList)
            ComparePrices2(currentCurrency)
            # print("Prev Prices X New Prices :", prevPriceList, newPriceList)
            csv_conversion.CsvFile(price, coin, fiat)


#rateOfChangeList = []
def ComparePrices2(currentCurrency):
    countPriceList = len(priceList)
    if countPriceList < 24:
        print("lista tar rata first time u inqas min 24 fil priceList[]")
        print("List count: ", countPriceList)
        prevPriceIndex = countPriceList - 7
        print("Prev price index :", prevPriceIndex)
        prevPrice = priceList[prevPriceIndex]
        newPrice = priceList[-1]
        print(currentCurrency, "'s Previous Price: ", prevPrice)
        print(currentCurrency, "'s Newest Price: ", newPrice)
        rateOfChange = (newPrice - prevPrice)/prevPrice
        print("Rate of Change of", currentCurrency, "is: ", rateOfChange)
        # percentage = "{:.2%}".format(rateOfChange)
        # print("Rate of Change of", currentCurrency, "in percentage is: ", percentage)
        # if (len(rateOfChangeList) <= 5):
        #     print("Rate of change list is smaller than 6.")
        #     rateOfChangeList.append(rateOfChange)
        #     print("rate of change list: ", rateOfChangeList)
        # elif (len(rateOfChangeList) >= 6):
        #     print("Rate of change list is greater than 6.")
        #     rateOfChangeList.append(rateOfChange)
        #     print("rate of change list: ", rateOfChangeList)
        #     CompareRateOfChange(currentCurrency)
        #rateOfChangeList.append(rateOfChange)
        roundROC = round(rateOfChange, 1)
        print(roundROC)
        #if roc >= rateOfChange or roc <= -rateOfChange:
        if prevPrice == newPrice:
            print("Rate stayed the same")
        elif rateOfChange > floatROC:
            #print(rateOfChange)
            GNS.send_to_gns("Rate Increased")
        elif rateOfChange < floatROC:
            #print(rateOfChange)
            GNS.send_to_gns("Rate Decreased")

    elif countPriceList >= 24:
        print("thalt hawn ghax wasalna 24 elements")
        print("List count: ", countPriceList)
        prevPriceIndex = countPriceList - 7
        print("Prev price index :", prevPriceIndex)
        prevPrice = priceList[prevPriceIndex]
        newPrice = priceList[-1]
        print(currentCurrency, "'s Previous Price: ", prevPrice)
        print(currentCurrency, "'s Newest Price: ", newPrice)
        rateOfChange = (newPrice - prevPrice) / prevPrice
        print("Rate of Change of", currentCurrency, "is: ", rateOfChange)
        # percentage = "{:.2%}".format(rateOfChange)
        # print("Rate of Change of", currentCurrency, "in percentage is: ", percentage)
        #rateOfChangeList.append(rateOfChange)
        #print("rate of change list: ", rateOfChangeList)
        roundROC = round(rateOfChange, 1)
        print(roundROC)
        if prevPrice == newPrice:
            print("Rate stayed the same")
        elif rateOfChange > floatROC:
            #print(rateOfChange)
            GNS.send_to_gns("Rate Increased")
        elif rateOfChange < floatROC:
            #print(rateOfChange)
            GNS.send_to_gns("Rate Decreased")
        del priceList[:12]
        print(countPriceList)




# def CompareRateOfChange(currentCurrency):
#     countRateList = len(rateOfChangeList)
#     print("Rate of change list count: ", countRateList)
#     preRateIndex = countRateList - 7
#     print("Prev price index :", preRateIndex)
#     prevRate = rateOfChangeList[preRateIndex]
#     newRate = rateOfChangeList[-1]
#     print(currentCurrency, "'s Previous Rate: ", prevRate)
#     print(currentCurrency, "'s Newest Rate: ", newRate)
#     if newRate > roc:
#         GNS.send_to_gns("Increased")
#     elif newRate < prevRate:
#         GNS.send_to_gns("Decreased")






# prevPriceList = []
# newPriceList = []
# def GetPrices():
#     url_price = "https://api.cryptowat.ch/markets/kraken/"
#     url_pair = "https://api.cryptowat.ch/pairs/"
#     priceString = "/price"
#     # tickers = 'btceur', 'etheur', 'ltceur'
#     # for loop that loops thorugh each currency with it's fiat
#     if not prevPriceList:
#         for ticker in combinedList:
#             print("Thalt l ewwel darba.")
#             currentCurrency = ticker
#             apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
#             apiUrlPair = requests.get(url_pair + currentCurrency)
#             # print(currentCurrency, ":", apiUrlPrice.json())
#             # print(currentCurrency, ':', apiUrlPair.json())
#             loadUrlPrice = json.loads(apiUrlPrice.text)
#             loadUrlPair = json.loads(apiUrlPair.text)
#             price = loadUrlPrice.get('result').get('price')
#             coin = loadUrlPair.get('result').get('base').get('symbol')
#             fiat = loadUrlPair.get('result').get('quote').get('symbol')
#             # print(coin, fiat)
#             print(currentCurrency, "price is:", price)
#             prevPriceList.append(price)
#             print("Prev Prices List: ", prevPriceList)
#             csv_conversion.CsvFile(price, coin, fiat)
#             # CheckPrices(price)
#     elif prevPriceList and newPriceList:
#         print("Thalt it tielet jew aktar min darba.")
#         prevPriceList.clear()
#         print("Suppost prev gie deleted: ", prevPriceList)
#         prevPriceList.extend(newPriceList)
#         print("Suppost new gie prev: ", prevPriceList)
#         newPriceList.clear()
#         print("Suppost new gie deleted: ", newPriceList)
#         for ticker in combinedList:
#             currentCurrency = ticker
#             apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
#             apiUrlPair = requests.get(url_pair + currentCurrency)
#             # print(currentCurrency, ":", apiUrlPrice.json())
#             # print(currentCurrency, ':', apiUrlPair.json())
#             loadUrlPrice = json.loads(apiUrlPrice.text)
#             loadUrlPair = json.loads(apiUrlPair.text)
#             price = loadUrlPrice.get('result').get('price')
#             coin = loadUrlPair.get('result').get('base').get('symbol')
#             fiat = loadUrlPair.get('result').get('quote').get('symbol')
#             # print(coin, fiat)
#             print(currentCurrency, "price is:", price)
#             newPriceList.append(price)
#             print("New Prices List:", newPriceList)
#             print("Prev Prices List:", prevPriceList)
#             CompareListsPrices(currentCurrency)
#             # print("Prev Prices X New Prices :", prevPriceList, newPriceList)
#             csv_conversion.CsvFile(price, coin, fiat)
#     else:
#         for ticker in combinedList:
#             print("Thalt it tieni darba.")
#             currentCurrency = ticker
#             apiUrlPrice = requests.get(url_price + currentCurrency + priceString)
#             apiUrlPair = requests.get(url_pair + currentCurrency)
#             # print(currentCurrency, ":", apiUrlPrice.json())
#             # print(currentCurrency, ':', apiUrlPair.json())
#             loadUrlPrice = json.loads(apiUrlPrice.text)
#             loadUrlPair = json.loads(apiUrlPair.text)
#             price = loadUrlPrice.get('result').get('price')
#             coin = loadUrlPair.get('result').get('base').get('symbol')
#             fiat = loadUrlPair.get('result').get('quote').get('symbol')
#             # print(coin, fiat)
#             print(currentCurrency, "price is:", price)
#             newPriceList.append(price)
#             print("New Prices List:", newPriceList)
#             print("Prev Prices List:", prevPriceList)
#             CompareListsPrices(currentCurrency)
#             # print("Prev Prices X New Prices :", prevPriceList, newPriceList)
#             csv_conversion.CsvFile(price, coin, fiat)
#
#
# prevRateOfChangeList = []
# newRateOfChangeList = []
#
#
# def CompareListsPrices(currentCurrency):
#     if len(prevRateOfChangeList) <= 5:
#         print("Thalt l ewwel darba fir rate.")
#         for new, prev in zip(newPriceList, prevPriceList):
#             rateOfChange = (new - prev) / prev
#         prevRateOfChangeList.append(rateOfChange)
#         print(new, prev)
#         print("Rate of Change in", currentCurrency, "is: ", rateOfChange)
#         # print("prev rate list: ", prevRateOfChangeList)
#
#     elif len(prevRateOfChangeList) > 5:
#         print("thalt it tieni darba fir rata")
#         for new, prev in zip(newPriceList, prevPriceList):
#             rateOfChange = (new - prev) / prev
#         newRateOfChangeList.append(rateOfChange)
#         print(new, prev)
#         print("Rate of Change in", currentCurrency, "is: ", rateOfChange)
#         print("new rate list: ", newRateOfChangeList)
#         print("prev rate list: ", prevRateOfChangeList)
#         for newRate, prevRate in zip(newRateOfChangeList, prevRateOfChangeList):
#             print(newRate, prevRate)
            # if newRate > prevRate:
            #     (currentCurrency, GNS.send_to_gns("increased rate"))
            # elif newRate == prevRate:
            #     print("Stayed the same, no notification")
            # elif newRate < prevRate:
            #     (currentCurrency, GNS.send_to_gns("decreased rate"))
    # elif len(prevRateOfChangeList == 5) and len(newRateOfChangeList == 5):
    #     print("thalt it tielet jew aktar fir rata")
    #     prevRateOfChangeList.clear()
    #     print("pre rate list deleted", prevRateOfChangeList)
    #     prevRateOfChangeList.extend(newRateOfChangeList)
    #     print("new rate list now prev rate list: ", prevRateOfChangeList)
    #     newRateOfChangeList.clear()
    #     print("new rate list deleted: ", newRateOfChangeList)
    #     for new, prev in zip(newPriceList, prevPriceList):
    #         rateOfChange = (new - prev) / prev
    #     newRateOfChangeList.append(rateOfChange)
    #     print(new, prev)
    #     print("Rate of Change in", currentCurrency, "is: ", rateOfChange)
    #     print("new rate list: ", newRateOfChangeList)
    #     print("prev rate list: ", prevRateOfChangeList)


# def SendNotif():
# if rateOfChange :
# GNS.send_to_gns("working")


Pairs()
RunMethod()

