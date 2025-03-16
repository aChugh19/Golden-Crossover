import pandas as pd
import sys
import requests
import json
# print(sys.argv)
# print(sys.argv[0])
apiKey = 'Z26uGb1ow7cWdqMBIgLy8QjvP7DSv5pG'
def getStockData(ticker,dateFrom,dateTo):
    stockdata = 'https://api.polygon.io/v2/aggs/ticker/'+ ticker + '/range/1/day/'+ dateFrom + '/' + dateTo + '?adjusted=true&sort=desc&apiKey='+ apiKey
    data = requests.get(stockdata).json()
    data = json.dumps(data)
    with open('./JSON_Files/'+ticker+'.json', 'w') as outfile:
        outfile.write(data)
    return

def getListOfTop50Stocks():
    return pd.read_csv('ind_nifty50list.csv')
    
