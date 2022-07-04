#知网文献整理
#知网文献爬虫时，只爬出了标准基本信息和相关图书
#标准之间的相互关系没有爬到。
import ast
import re

import pandas as pd
import numpy as np

df=pd.read_csv('zhi.csv',encoding='gbk',header=0)
print(len(df))
drop_index=[]
for i in range(len(df)):
    if df['title'][i]=='[]':
        drop_index.append(i)
    else:
        pass
print(drop_index)
df2=df.drop(drop_index,axis=0)
print(df2.head(3))
print(len(df2))
df2.to_csv("zhi2.csv",index=False,encoding='gbk')
new_dict={
    '标准中文名':[],
    '标准英文名':[],
    '基本信息':[],
    '相关图书':[]
}
for i in range(len(df2)):
    newbs={}
    try:
        title=ast.literal_eval(df2['title'][i])
        pattern1=r'>([\u4e00-\u9fa5]+.+?)<'
        chiname=re.findall(pattern1,title[0],re.M|re.S|re.I)
        if chiname:
            if '<a' in chiname[0]:
                chiname=re.findall('(.+?)<a class',chiname[0],re.M|re.S|re.I)
                new_dict['标准中文名'].append(chiname[0])
            else:
                new_dict['标准中文名'].append(chiname[0])

        pattern2=r'<span>(.+?)</span>'
        engname=re.findall(pattern2,title[0],re.M|re.S|re.I)
        if engname:
            new_dict['标准英文名'].append(engname[0])

        basic=ast.literal_eval(df2['basic'][i])
        basicval=list(basic.values())
        newbasicval=[]
        for j in range(len(basicval)):
            if basicval[j]!=None:
                j=re.sub('<a.+?</a>','',basicval[j][0],re.M|re.I|re.S)
                newbasicval.append(j)
            else:
                newbasicval.append(None)
        basickey=list(basic.keys())
        for k,v in zip(basickey,newbasicval):
            newbs[k]=v

        new_dict['基本信息'].append(newbs)
        newbook={
            '书名':[],
            '作者':[]
        }
        book=df2['relation_books'][i]
        if type(book)==str:
            books=book.split('\n')
            if len(books)==10:
                newbook['书名'].append(books[0])
                newbook['作者'].append(books[1])
                newbook['书名'].append(books[4])
                newbook['作者'].append(books[5])
                newbook['书名'].append(books[6])
                newbook['作者'].append(books[7])
                newbook['书名'].append(books[8])
                newbook['作者'].append(books[9])
                new_dict['相关图书'].append(newbook)
            else:
                new_dict['相关图书'].append(newbook)
        else:
            new_dict['相关图书'].append(newbook)
    except:
        print('第{}条数据解析错误'.format(i))
Data=pd.DataFrame(new_dict)
Data.to_csv("new_zhi.csv",encoding='gbk',index=False)
