import pandas as pd
import dateListgenerator
import os
dates = dateListgenerator.getDates(startDate='2020-01-01', endDate='2023-03-24')
dict={}
for date in dates:
    year,month,d = date.split('-')
    if os.path.exists('./2020to2023/'+str(d)+str(month)+str(year)+'.csv'):
        dateWiseData = pd.read_csv('./2020to2023/'+str(d)+str(month)+str(year)+'.csv')
        for i in range(len(dateWiseData)):
            if dateWiseData['SYMBOL'][i] not in dict:
                dict[dateWiseData['SYMBOL'][i]] = pd.DataFrame(columns=['date','open','close','high','low','deliveryPerc'])
            dict[dateWiseData['SYMBOL'][i]].loc[len(dict[dateWiseData['SYMBOL'][i]])] = [date,dateWiseData[' OPEN_PRICE'][i],dateWiseData[' CLOSE_PRICE'][i],dateWiseData[' HIGH_PRICE'][i],dateWiseData[' LOW_PRICE'][i],dateWiseData[' DELIV_PER'][i]] 
        print(date+' Done.')    

for ticker in dict.keys():
    if(len(dict[ticker])>50):
        dict[ticker].to_csv('./Stock Data/'+ticker+'.csv',index=False)
        print(ticker+' Done.')

