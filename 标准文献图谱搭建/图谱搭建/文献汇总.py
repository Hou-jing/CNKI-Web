#三个文件安装标准名统一在一个文件中
import re

import pandas as pd

df1=pd.read_csv('new_信息网.csv',encoding='utf_8',header=0)
infor_name=df1['标准名']
df2=pd.read_csv('new_zhi.csv',encoding='gbk',header=0)
zhi_name=df2['标准中文名']
df3=pd.read_csv('new_参考文献.csv',encoding='gbk',header=0)
infer_name=df3['标准名']

l1=infor_name.tolist()
l2=zhi_name.tolist()
l3=infer_name.tolist()

print('1和2相同的标准名有{},共有{}条'.format(set(l1)&set(l2),len(set(l1)&set(l2))))
print('2和3相同的标准名有{},共有{}条'.format(set(l2)&set(l3),len(set(l1)&set(l2))))
print('1和3相同的标准名有{},共有{}条'.format(set(l1)&set(l3),len(set(l1)&set(l2))))


for i in range(len(infor_name)):
    df1['标准名'][i]=re.sub('\s',' ',df1['标准名'][i],re.M|re.S|re.I)

for i in range(len(zhi_name)):
    df2['标准中文名'][i] = re.sub('\s', ' ', df2['标准中文名'][i], re.M | re.S | re.I)

for i in range(len(infer_name)):
    df3['标准名'][i]=re.sub('\s','',df3['标准名'][i],re.M | re.S | re.I)

infor_name=df1['标准名']
zhi_name=df2['标准中文名']
infer_name=df3['标准名']

l1=infor_name.tolist()
l2=zhi_name.tolist()
l3=infer_name.tolist()

print('1和2相同的标准名有{},共有{}条'.format(set(l1)&set(l2),len(set(l1)&set(l2))))
print('2和3相同的标准名有{},共有{}条'.format(set(l2)&set(l3),len(set(l1)&set(l2))))
print('1和3相同的标准名有{},共有{}条'.format(set(l1)&set(l3),len(set(l1)&set(l2))))

df2=df2.rename(columns={'标准中文名':'标准名'})

print('df2的列名是{}'.format(df2.columns))
df4=pd.merge(df1,df2,how='outer',on='标准名')
print(df4.head(3))
df5=pd.merge(df4,df3,how='outer',on='标准名')
print('df5的列名是{}'.format(df5.columns))

df5.to_csv('标准合.csv',index=False,encoding='gbk')


