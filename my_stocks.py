# import dependencies
import pandas as pd
import random
import statistics
import numpy
import requests
import matplotlib.pyplot as plt
from datetime import date, timedelta

# import api key
from config import key

my_symbols = ['AAPL', 'TSLA', 'FB', 'MSFT', 'NVDA']
money_invested = [10, 142.6, 30, 25, 20]
yesterday_date = date.today() - timedelta(1)

# create a base url from polygon.io
base_url = 'https://api.polygon.io/v1/open-close/'

# create an empty list to hold all of the urls
url_list = []
# loop through the symbols and create a list of the urls
for symbol in my_symbols:
    url_list.append(f'{base_url}{symbol}/{yesterday_date}/?adjusted=false&apiKey={key}')

# create an empty list to hold the results in json format
res = []
# loop through the url_list and request the information
for url in url_list:
    res.append(requests.get(url).json())

# lists that will create the df
stock_close = []
stock_open = []
percent_change = []
stock_symbol = []

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
    'symbol': stock_symbol,
    'amount invested': money_invested,
    'open': stock_open,
    'close': stock_close,
    'percent change': percent_change
}

# put the dictionary into a df for easier viewing
my_stocks_df = pd.DataFrame(stock_dict)

# print the df
print(my_stocks_df)

# create a horizontal bar chart that shows the percent change for each of the stocks to see which did the best
plt.barh(stock_symbol, height = 0.4, width = percent_change, color = 'r')
# annotate the chart
plt.title(f'Percent Change for {yesterday_date}')
plt.xlabel('Stock Symbol')
plt.ylabel('Percent Change')

# show the chart
plt.show()

# save the stocks for that day into a dictionary
today = date.today()
daily_dict = {f'{today}': stock_dict}
