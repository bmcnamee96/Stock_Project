# import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import requests

# import api key
from config import key

# have the user input what they want to see
stock_input = input('What stock do you want to find?')
start_input = input('What is the start day? ("YYYY-MM-DD")')
end_input = input('What is the end day? ("YYYY-MM-DD")')
# for testing:
# stock_input = 'TSLA'
# start_input = '2022-04-01'
# end_input = '2022-04-12'

# request the api from polygon
# using the base url from polygon docs
base_url = 'https://api.polygon.io/v2/aggs/ticker/'

# create the url that will be put into json including api key
url = f'{base_url}{stock_input}/range/1/day/{start_input}/{end_input}?adjusted=false&sort=asc&limit=1900&apiKey={key}'

# get the text in json format in result
result = requests.get(url).json()
# print(result)

# get the status of the stock
status = result['status']

# create a list to hold the close prices for the stock
close_prices = []

# create the loop to show me the close price for each day
for day in result['results']:
    for close, price in day.items():
        if close == 'c':
            close_prices.append(price)

# create a line chart
plt.plot(close_prices, color = 'r')
# give x and y labels and a title
plt.xlabel('Number of Days')
plt.ylabel('Price')
plt.title(f'Change in Price for {stock_input} \n from {start_input} - {end_input}')

# make a textbox that shows the status of the stock
x_position = len(close_prices)/2
y_position = np.max(close_prices)
plt.text(x_position, y_position, (f'Status: {status}'), fontsize=10, verticalalignment='top')

# show the graph
plt.show()