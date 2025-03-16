import os
import numpy as np
import pandas as pd
ec=0
dc=0
for f in os.listdir('./Stock Data'):
    df = pd.read_csv('./Stock Data/'+f)
    if df['date'][len(df)-1]==df['date'][len(df)-2]:
        fs = open('./Stock Data/'+f, "r+")
        lines = fs.readlines()
        lines.pop()
        fs = open('./Stock Data/'+f, "w+")
        fs.writelines(lines)
        dc+=1
        print(f+' duplicate found. Date:' + df['date'][len(df)-1])
print('empty count: ',ec)
print('dupli coun: ',dc)