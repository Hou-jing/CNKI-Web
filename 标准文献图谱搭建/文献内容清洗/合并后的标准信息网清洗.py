
#清洗汇总后的all.csv文件。
import ast
import re

import pandas as pd
newdf={
    '标准名':[],
    '标准类型':[],
    '标准性质':[],
    '标准状态':[],
    '起草单位':[],
    '起草人':[],
    '基本信息':[],
    '相近标准':[],
    '标准详情':[]
}
df=pd.read_csv('all.csv',encoding='gbk',header=0)
# print(df.head)
print(df.index)

for i in range(len(df['draft_name'])):
    name=ast.literal_eval(df['draft_name'][i])
    info=ast.literal_eval(df['label_info'][i])
    succ=ast.literal_eval(df['label_success'][i])
    prim=ast.literal_eval(df['label_primary'][i])

    newdf['标准名'].append(name[0])
    newdf['标准类型'].append(info[0])
    newdf['标准性质'].append(succ[0])
    newdf['标准状态'].append(prim[0])
    newdf['标准详情'].append(df['draft_url'][i])
    draftunit=ast.literal_eval(df['draft_unit'][i])
    units=[]
    for unit in draftunit[1:]:
        u=unit.replace('\n','').replace('\t','').replace('\r','')
        if u!='' and u!=' 、' and u!='、' and u!= '。' and u!='、' and u!=' 、' and u!=' 。':
            units.append(u)
    newdf['起草单位'].append(units)
    draftper= ast.literal_eval(df['draft_person'][i])
    pers=[]
    for per in draftper[1:]:
        p=per.replace('\n','').replace('\t','').replace('\r','')
        if p!='' and p!=' 、'and p!='、' and p!=' 、' and p!=' 。':
            pers.append(p)
    newdf['起草人'].append(pers)
    newdf['基本信息'].append(ast.literal_eval(df['basic_information'][i]))
    rela_items=ast.literal_eval(df['basic_info_items'][i])
    nums=len(rela_items[0])
    rel_item={
        '标准号':[],
        '标准名':[],
        '标准网址':[]
    }
    for i in range(nums):
        rel_item['标准号'].append(rela_items[1][i])
        rel_item['标准名'].append(rela_items[2][i][0])
        rel_item['标准网址'].append(rela_items[0][i])
    newdf['相近标准'].append(rel_item)



DataDraft=pd.DataFrame(newdf)
DataDraft.to_csv('new_信息网.csv',encoding='gbk',index=False)






