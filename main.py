import pandas as pd
import getNifty50StockData
import processJsonFile
import feature_movingAverage
import plotCandleSticks
import time

niftyStocks = pd.read_csv('C:\\Users\\asus\\Desktop\\Stock Market Scripts\\ind_nifty50list.csv')
counter=1
for ticker in niftyStocks['Symbol']:
    ticker='BSE: HDFCBANK'
    print(ticker)
    getNifty50StockData.getStockData(ticker=ticker, dateFrom='2005-01-01', dateTo='2023-03-20')
    processJsonFile.exportasCSV(ticker=ticker, dateFrom='2005-01-01', dateTo='2023-03-20')
    feature_movingAverage.addFeature(ticker, feature='ma_50')
    feature_movingAverage.addFeature(ticker, feature='ma_200')
    plotCandleSticks.exportChart(ticker, features=['ma_50','ma_200'])
    print(str(counter)+'. '+ticker+' Done.\n')
    counter+=1
    break
    time.sleep(70)

    