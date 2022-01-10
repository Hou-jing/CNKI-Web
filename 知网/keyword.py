import matplotlib.pyplot as plt
import pandas as pd
df=open('keywords.csv',encoding='utf_8')
print(type(df))
key=[]
num=[]
for line in df:
    line=line.split(' ')
    key.append(line[0].split('\t')[1])
    num.append(line[0].split('\t')[2])
print(num,key)
num=num[1:]
key=key[1:]
import csv
f=open('关键词.csv','w',encoding='utf_8')
csv_writer=csv.writer(f)
f.write('{},{}\n'.format('key','num'))
for i in range(len(num)):
    f.write('{},{}\n'.format(key[i],num[i]))
f.close()
df2=pd.read_csv('关键词.csv',encoding='utf_8')
import numpy as np
df2.sort_values('num',ascending=False,inplace=True)
df2.to_csv('rank_key.csv')
df3=pd.read_csv('rank_key.csv',encoding='utf_8')
print(key,num)

plt.rcParams['font.family']=['SimHei']
plt.barh(df3['key'][1:25],df3['num'][1:25],color='blue')
plt.xlabel('词频')
plt.ylabel('关键词')
plt.show()
# plt.bar(num,key)
# plt.show()