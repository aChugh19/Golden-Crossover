import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import date
from datetime import datetime
import os
import random as r

def displayChart(ticker,days=None,features=['ma_44','ma_200']):
    color ={'ma_44':'#808080','ma_200':'#0000FF'}
    df = pd.read_csv('./top250 Stock Data/'+ticker+'.csv')
    if days!=None:
        df = df[-1*days:]
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'])
                        ])

    for feature in features:
        fig2 = px.line(x = df['date'] ,y = df[feature])
        fig2.update_traces(line_color=color[feature])
        fig = go.Figure(fig.data+fig2.data)      

    fig.update_layout(xaxis_rangeslider_visible=False)
    
    today = date.today()
    if not os.path.exists('./plots/'+str(today)):
        os.makedirs('./plots/'+str(today))

    fig.write_image('./plots/'+str(today)+'/'+ticker+'_'+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+'.png')  
    fig.show()

# displayChart(ticker='NIACL',days=100)