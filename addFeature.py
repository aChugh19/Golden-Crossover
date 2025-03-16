import feature_movingAverage
import os
import pandas as pd
i=22
# for ticker in os.listdir('./Stock Data')[10:]:
#     df = pd.read_csv('./Stock Data/'+ticker)
#     if len(df)<220:
#         i+=1
#         os.remove('./Stock Data/'+ticker)
#         # print(ticker)
# print(i)
# print(len(os.listdir('./Stock Data')))
#         
for ticker in os.listdir('./Stock Data')[22:]:
    print(ticker.split('.')[0]+' Started.'+':'+str(i))
    i+=1
    feature_movingAverage.addFeature(ticker.split('.')[0], feature='ma_44')
    feature_movingAverage.addFeature(ticker.split('.')[0], feature='ma_200')
#3,9,24    