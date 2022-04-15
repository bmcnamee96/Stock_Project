# import dependencies
import pandas as pd
import requests
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook
from openpyxl import load_workbook

# import api key
from config import key

my_symbols = ['AAPL', 'TSLA', 'FB', 'MSFT', 'NVDA']
dates = ['2022-04-01', 
    '2022-04-04', '2022-04-05','2022-04-06', '2022-04-07' '2022-04-08', 
    '2022-04-11', '2022-04-12', '2022-04-13', '2022-04-14']

# create a base url from polygon.io
base_url = 'https://api.polygon.io/v1/open-close/'

# create an empty list to hold all of the urls
url_list = []
# create an empty list to hold the results in json format
res = []
# lists that will create the df
stock_close = []
stock_open = []
percent_change = []
stock_symbol = []

# loop through the symbols and create a list of the urls
for x in dates:
    for symbol in my_symbols:
        url_list.append(f'{base_url}{symbol}/{x}/?adjusted=false&apiKey={key}')

# loop through the url_list and request the information
for url in url_list:
    res.append(requests.get(url).json())

# fill the lists close, open, symbol
for stock_info in res:
    for key, value in stock_info.items():
        if key == 'close':
            stock_close.append(value)
        if key == 'open':
            stock_open.append(value)
        if key == 'symbol':
            stock_symbol.append(value)

# find the percent_change for each stock
i = 0
length = len(stock_symbol)
# use a while loop to loop through the data
while i < length:
    day_dif = stock_close[i] - stock_open[i]
    percent_change.append(day_dif / stock_close[i] * 100)
    
    i += 1

# create a dict
stock_dict = {
    'date': dates,
    'symbols': my_symbols,
    'open': stock_open,
    'close': stock_close,
    'percent change': percent_change
}

# save the stocks for that day into an excel file
# use a while loop to loop through all of the data and save it into the excel file

i = 0

while i < len(stock_symbol):
    daily_stock = []
    daily_stock.append(stock_symbol[i])
    daily_stock.append(dates)
    daily_stock.append(stock_open[i])
    daily_stock.append(stock_close[i])
    daily_stock.append(percent_change[i])

    # append the excel file and add the data onto it
    workbook_name = 'testing.xlsx'
    wb = load_workbook(workbook_name)
    page = wb.active

    # new data to write
    new_daily_stock = [daily_stock]

    for info in new_daily_stock:
        page.append(info)
    
    # save the excel file
    wb.save(filename=workbook_name)

    i += 1


