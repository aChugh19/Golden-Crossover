import json
import pandas as pd
import dateListgenerator

def exportasCSV(ticker,dateFrom,dateTo):
    with open('./JSON_Files/'+ticker+'.json') as json_file:
        data = json.load(json_file)
    df = pd.DataFrame(columns=['date','open','close','high','low'])    
    for daydata in data['results']:
        df.loc[len(df.index)] = ['',daydata['o'],daydata['c'],daydata['h'],daydata['l']] 
    df['date'] = dateListgenerator.getDates(dateFrom,dateTo)[:len(data['results'])]   
    df.to_csv('./CSV_Files/'+ticker+'.csv',index=False)
           
