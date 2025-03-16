import json
import pandas as pd
import os

upTrend = json.load(open('SuccessPer_UPTrend.json'))
downTrend = json.load(open('SuccessPer_DownTrend.json'))
merged = json.load(open('SuccessPer.json'))
df = pd.DataFrame(columns=['Stock','merged','Total_true','Total_false','UpTrend_Per','Up_True','Up_false','DownTrend_Per','down_True','down_False'])

for ticker in os.listdir('./top250 Stock Data'):
    up,up_true,up_false  = (upTrend[ticker][0],upTrend[ticker][1],upTrend[ticker][2]) if ticker in upTrend.keys() else (-1,-1,-1)
    down,down_true,down_false  = (downTrend[ticker][0],downTrend[ticker][1],downTrend[ticker][2]) if ticker in downTrend.keys() else (-1,-1,-1)
    merge,total_true,total_false  = (merged[ticker][0],merged[ticker][1],merged[ticker][2]) if ticker in merged.keys() else (-1,-1,-1)
    # print(up,up_true,up_false)  
    # print(down,down_true,down_false)
    # print(merge,total_true,total_false)
    df.loc[len(df)] = [ticker,merge,total_true,total_false,up,up_true,up_false,down,down_true,down_false]

df.to_csv('SuccessPercentage.csv',index=False)

