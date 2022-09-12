import csv
import time
import os

filename = "Prices.csv"


def CsvFile(price, coin, fiat):
    if os.path.exists(filename):
        with open('Prices.csv', 'a', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Coin', 'Fiat', 'Price']
            the_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            the_writer.writerow({'Timestamp': time.time(), 'Coin': coin.upper(), 'Fiat': fiat.upper(), 'Price': price})
    else:
        CreateCSVFile(price, coin, fiat)


def CreateCSVFile(price, coin, fiat):
    with open('Prices.csv', 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Coin', 'Fiat', 'Price']
        the_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        the_writer.writeheader()
        the_writer.writerow({'Timestamp': time.time(), 'Coin': coin.upper(), 'Fiat': fiat.upper(), 'Price': price})
