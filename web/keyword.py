import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv('keyword.csv',encoding='utf_8',header=None)
print(type(df))
key=[]
num=[]
for i in range(len(df)):
    line=str(df.loc[i,0])
    line=line.split('\t')
    num.append(line[2])
    key.append(line[1])
# print(num,key)
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
key=open('key.txt','w',encoding='utf_8')
for i in df3['key']:
    key.write('{}\n'.format(i))
#翻译
# from pygtrans import Translate
# client=Translate()
# Chinese=[]
# for i in df3['key']:
#     c=client.translate(i)
#     Chinese.append(c)
#     print(c)
# df3['翻译']=Chinese
import matplotlib.font_manager as fm
for font in fm.fontManager.ttflist:
  print(font.name)
plt.rcParams['font.family']=['SimHei']
# plt.rcParams['font.family']=['Times New Roman']
plt.barh(df3['key'][0:25],df3['num'][0:25],color='blue')

plt.xlabel('词频')
plt.ylabel('关键词')
plt.show()
# plt.bar(num,key)
# plt.show()