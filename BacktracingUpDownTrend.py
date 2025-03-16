import pandas as pd
import telegramApi
import os
import numpy as np
import json
import sys

upTrendStock=[]
downTrendStock=[]
tradeready=[]
tradeready_sf=[]
tickerSuccess = {}

def tradeReadyStocks(df,trend,ticker):
    if trend=='Up':
        if not df['close'][len(df)-1]>=df['open'][len(df)-1] \
            or not df['low'][len(df)-1] < (df['ma_44'][len(df)-1]+(df['ma_44'][len(df)-1])*0.005)\
            or not df['high'][len(df)-1] > df['ma_44'][len(df)-1]:
            return
        buy = df['high'][len(df)-1]+(df['high'][len(df)-1])*0.003
        stopLoss= min(df['low'][len(df)-1],df['low'][len(df)-2])
        target=buy+(buy-stopLoss)*2
        tradeready.append((ticker,trend,buy,target,stopLoss))
    elif trend=='Down':
        if not df['close'][len(df)-1]<=df['open'][len(df)-1] \
            or not df['high'][len(df)-1] > (df['ma_44'][len(df)-1]-(df['ma_44'][len(df)-1])*0.005)\
            or not df['low'][len(df)-1] < (df['ma_44'][len(df)-1]):
            return
        buy = df['low'][len(df)-1]-(df['low'][len(df)-1])*0.003
        stopLoss= max(df['high'][len(df)-1],df['high'][len(df)-2])
        target=buy - (stopLoss-buy)*2
        tradeready.append((ticker,trend,buy,target,stopLoss))
    return     

def trendList(df,ticker):
    if(df['ma_44'][len(df)-1]>df['ma_44'][len(df)-2]):
        uptrend=True
    else:
        uptrend=False
    vtc = df['ma_44'][len(df)-1]
    tl=0
    ma_44_lis = list(df['ma_44'])
    ma_44_lis.reverse() 
    for i in zip(ma_44_lis):
        # print(i,vtc)
        if uptrend and i<=vtc:
            tl+=1
        elif not uptrend and i>=vtc:
            tl+=1
        else:
            break
        vtc=i
    # print(ticker,tl)
    if uptrend:
        if tl>15:
            tradeReadyStocks(df, 'Up', ticker)
        upTrendStock.append((tl,ticker))
    else:
        if tl>15:
            tradeReadyStocks(df, 'Down', ticker)
        downTrendStock.append((tl,ticker))    
    return

def check_sf(df,trend,buy,target,SL,start):
    # print(df)
    if buy<df['low'][start] or buy>df['high'][start]:
        return None

    for i in range(start, start+len(df)):
        if Upflag and  trend=='Up':
            if df['high'][i]>=target:
                # print(df['date'][i])
                return True
            if df['low'][i]<=SL:
                # print(df['date'][i])
                return False    
        elif not Upflag and trend=='Down':
            if df['low'][i]<=target:
                # print(df['date'][i])
                return True
            if df['high'][i]>=SL:
                # print(df['date'][i])
                return False
    return None

if len(sys.argv)==1:
    print('Please pass trend as Arguement.\n1.Up\n2.Down')
    exit()
elif sys.argv[1] not in ['Up','Down']:
    print('Please pass trend correctly.\n1.Up\n2.Down')
    exit()
if sys.argv[1]=='Up':
    Upflag=True
else:
    Upflag=False

for ticker in os.listdir('./top250 Stock Data/'):
    print(ticker)
    df_sample = pd.read_csv('./top250 Stock Data/'+ticker)
    pl = len(tradeready)
    for i in range(20,len(df_sample)-2):
        df = df_sample[:i+1]
        trendList(df,ticker.split('.')[0])
        if len(tradeready)>pl:
            pl=len(tradeready)
            tradeready_sf.append(check_sf(df_sample[i+1:], trend=tradeready[-1][1], buy=tradeready[-1][2],target=tradeready[-1][3], SL=tradeready[-1][4],start=i+1))
            # print(tradeready_sf[-1],'\n')
    # print(tradeready_sf)
    if tradeready_sf.count(1)+tradeready_sf.count(0)!=0:
        tickerSuccess[ticker] = float("{:.2f}".format((tradeready_sf.count(1)*100)/(tradeready_sf.count(1)+tradeready_sf.count(0))))
    tradeready=[]
    tradeready_sf=[]   
    
# Data to be written
if Upflag: # print(tickerSuccess)    
    with open("UptrendSuccess.json", "w") as outfile:
        json.dump(tickerSuccess, outfile)
else:
    with open("DowntrendSuccess.json", "w") as outfile:
        json.dump(tickerSuccess, outfile)

