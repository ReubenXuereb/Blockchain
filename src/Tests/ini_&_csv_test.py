from configparser import ConfigParser
import csv

config = ConfigParser()

config.read(r'C:\Users\rubxu\Desktop\recruitment-2022-python-ReubenXuereb-main\config\config.ini')
# print(config.sections())

roc = config.get('general', 'rate_of_change')
tps = config.get('general', 'time_period_seconds')
cc = config.get('general', 'cryptocurrencies')
currency_list = cc.split(',')
fiat = config.get('general', 'fiat')
fiat_list = fiat.split(',')
# print(roc)
# print(tps)
# print(cc)
# print(currency_list)
# print(fiat)
# print(fiat_list)

combined_list = []
for currency in currency_list:
    for symbol in fiat_list:
        combination = currency + symbol
        print(combination)
        combined_list.append(combination)
print("Combination list: ", combined_list)

with open('test1.csv', 'w', newline='') as csvfile:
    fieldnames = ['Timestamp', 'Coin', 'Fiat', 'Price']

    theWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    theWriter.writeheader()

    theWriter.writerow({'Timestamp': 'timestamp', 'Coin': 'Unix timestamp format (seconds since Jan 01 1970 UTC)',
                        'Fiat': '12/08/2022', 'Price': '10'})

# with open('test2.csv', 'w', newline='') as csvfile2:
# fieldnames = ['roc', 'tps']

# theWriter = csv.DictWriter(csvfile2, fieldnames=fieldnames)
# theWriter.writeheader()

# theWriter.writerow({'roc': roc, 'tps': tps})
