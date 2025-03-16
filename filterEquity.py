import csv
import os
for f in os.listdir('./2021to2023'):
    inputf = open('./2021to2023/'+f, 'r')
    outputf = open('./2020to2023/'+f, 'w',newline='')
    writer = csv.writer(outputf)
    flag=True
    for row in csv.reader(inputf):
        if flag:
            writer.writerow(row)
            flag=False
        if row[2].strip()=='EQ':
            writer.writerow(row)    
    inputf.close()
    outputf.close()
    print(f+' done.')