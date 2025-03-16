import numpy as np 
import pandas as pd 

def movingAverage(ticker,days,feature):
    df = pd.read_csv('./top250 Stock Data/'+ticker+'.csv')
    ma=0
    tempList=[]
    for i in range(days):
        ma+=df['close'][i]
        tempList.append(ma/(i+1))
    for i in range(days,len(df['close'])):
        ma-=df['close'][i-days]
        ma+=df['close'][i]
        tempList.append(ma/days)
    df[feature]=tempList[:len(df['close'])]
    df.to_csv('./top250 Stock Data/'+ticker+'.csv',index=False)    
    return

def addFeature(ticker,feature):
    if feature=='ma_50':
        movingAverage(ticker,50,feature)
    elif feature=='ma_200':
        movingAverage(ticker,200,feature)
    elif feature=='ma_44':
        movingAverage(ticker,44,feature)
