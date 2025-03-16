import json
import pandas as pd
import os
import telegramApi
c=0
d=0 
x = json.load(open('UptrendSuccess.json'))       
for ticker in os.listdir('./top250 Stock Data'):
    if ticker in x.keys() and x[ticker]>=75:
        print(ticker)
        c+=1

print('\n\nDown\n\n')
x = json.load(open('DowntrendSuccess.json'))       
for ticker in os.listdir('./top250 Stock Data'):
    if ticker in x.keys() and x[ticker]>=75:
        print(ticker)
        d+=1

print(c,'\n',d)        