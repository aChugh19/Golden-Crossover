import json
import os
import pandas as pd
import numpy as np

delDict = {}
for ticker in os.listdir('./top250 Stock Data'):
    df = pd.read_csv('./top250 Stock Data/'+ticker)
    delDict[ticker] = float("{:.2f}".format(np.average(df['deliveryPerc'][-100:])))

with open("AverageDelivery.json", "w") as outfile:
    json.dump(delDict, outfile)