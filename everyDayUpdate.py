import datetime
import sys
import os
import pandas as pd
import dateListgenerator
from csv import writer
import numpy as np
import telegramApi
import json

def trendList(ticker):
    df = pd.read_csv('./top250 Stock Data/'+ticker+'.csv')
    if df['ma_44'][len(df)-1]>df['ma_44'][len(df)-2]:
        uptrend=True
    else:
        uptrend=False
    
    vtc = df['ma_44'][len(df)-1]
    tl=0    
    ma_44_lis = list(df['ma_44'])
    ma_44_lis.reverse()
    for i in ma_44_lis:
        # print(i,vtc)
        if uptrend and i<=vtc:
            tl+=1
        elif not uptrend and i>=vtc:
            tl+=1
        else:
            break
        vtc=i
        
    if uptrend:
        if tl>15:
            tradeReadyStocks(df, 'Up', ticker)
        # upTrendStock.append((tl,ticker))
    else:
        if tl>15:
            tradeReadyStocks(df, 'Down', ticker)
        # downTrendStock.append((tl,ticker))        
    return

def tradeReadyStocks(df,trend,ticker):
    if trend=='Up':
        if not df['close'][len(df)-1]>=df['open'][len(df)-1] \
            or not df['low'][len(df)-1] < (df['ma_44'][len(df)-1]+(df['ma_44'][len(df)-1])*0.005)\
            or not df['high'][len(df)-1] > df['ma_44'][len(df)-1]:
            return
        buy = df['high'][len(df)-1]+(df['high'][len(df)-1])*0.003
        stopLoss= min(df['low'][len(df)-1],df['low'][len(df)-2])
        target=buy+(buy-stopLoss)*2
        tradeready.append((ticker,trend,float("{:.2f}".format(buy)),float("{:.2f}".format(target)),float("{:.2f}".format(stopLoss))))
    elif trend=='Down':
        if not df['close'][len(df)-1]<=df['open'][len(df)-1] \
            or not df['high'][len(df)-1] > (df['ma_44'][len(df)-1]-(df['ma_44'][len(df)-1])*0.005)\
            or not df['low'][len(df)-1] < (df['ma_44'][len(df)-1]):
            return
        buy = df['low'][len(df)-1]-(df['low'][len(df)-1])*0.003
        stopLoss= max(df['high'][len(df)-1],df['high'][len(df)-2])
        target=buy - (stopLoss-buy)*2
        tradeready.append((ticker,trend,float("{:.2f}".format(buy)),float("{:.2f}".format(target)),float("{:.2f}".format(stopLoss))))
    return      
      
def filtertradeready(tradeready):
    pop=[]
    for ticker,trend,x,y,z in tradeready:
        if trend=='Up':
            successPer = json.load(open('UptrendSuccess.json'))
        else:
            successPer = json.load(open('DowntrendSuccess.json'))
        if ticker+'.csv' in successPer.keys() and successPer[ticker+'.csv']>=75:
            continue
        else:
            pop.append((ticker,trend,x,y,z))
    
    for i in pop:
        tradeready.remove(i)
        
    return
    
def checkDeliveryPerc():
    averageDeliPer = json.load(open('AverageDelivery.json'))
    for ticker in os.listdir('./top250 Stock Data'):
        df = pd.read_csv('./top250 Stock Data/' + ticker)
        if averageDeliPer[ticker]+10 < df['deliveryPerc'][len(df)-1]:
            telegramApi.deliveryTrades(ticker, avg=averageDeliPer[ticker], now=df['deliveryPerc'][len(df)-1])
    return

if len(sys.argv)!=1:
    date = sys.argv[1]
else:
    date = str(datetime.datetime.today()).split(' ')[0]

year,month,d = date.split('-')
upTrendStock=[]
downTrendStock=[]
tradeready = []

if datetime.datetime(int(year),int(month),int(d)).weekday() in [5,6]\
    or date in dateListgenerator.allHolidays:
    print("Market Closed Today.")
else:
    print(date)
    url = "https://archives.nseindia.com/products/content/sec_bhavdata_full_"+str(d)+str(month)+str(year)+".csv"
    dateWiseData = pd.read_csv(url)
    stocks = os.listdir('./top250 Stock Data/')
    for i in range(len(dateWiseData)):
        if dateWiseData[' SERIES'][i].strip()!='EQ':
            continue
        if dateWiseData['SYMBOL'][i]+'.csv' in stocks:
            df = pd.read_csv('./top250 Stock Data/'+dateWiseData['SYMBOL'][i]+'.csv')
            ma_44 = (np.sum(df['close'][-43:])+dateWiseData[' CLOSE_PRICE'][i])/44
            ma_200 = (np.sum(df['close'][-199:])+dateWiseData[' CLOSE_PRICE'][i])/200
            List = [date,dateWiseData[' OPEN_PRICE'][i],dateWiseData[' CLOSE_PRICE'][i],dateWiseData[' HIGH_PRICE'][i],dateWiseData[' LOW_PRICE'][i],dateWiseData[' DELIV_PER'][i],ma_44,ma_200] 
            with open('./top250 Stock Data/'+dateWiseData['SYMBOL'][i]+'.csv', 'a',newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
            df = pd.read_csv('./top250 Stock Data/'+dateWiseData['SYMBOL'][i]+'.csv')
            trendList(dateWiseData['SYMBOL'][i])
            print(dateWiseData['SYMBOL'][i]+' Done.')

    # upTrendStock = [(days,ticker) for days,ticker in upTrendStock if days>5]
    # downTrendStock = [(days,ticker) for days,ticker in downTrendStock if days>5]
    # upTrendStock.sort()
    # downTrendStock.sort()
    # telegramApi.trendStocks(lis=upTrendStock, trend='upTrend',date=date)
    # telegramApi.trendStocks(lis=downTrendStock, trend='downTrend',date=date)
    filtertradeready(tradeready)
    telegramApi.trades(lis=tradeready, date=date)

