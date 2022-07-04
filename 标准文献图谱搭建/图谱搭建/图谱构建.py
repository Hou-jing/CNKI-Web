#对于合并之后的文件，信息做再加工
#搭建标准图谱

import ast
import time

import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher
#去重操作
# df=pd.read_csv('标准合.csv',encoding='gbk',header=0)
# df2=df.drop_duplicates(subset=['标准名'],keep='first', inplace=False)
# df2.to_csv('标准合2.csv',encoding='gbk',header=df.columns,index=False)
#
graph = Graph(
        "http://localhost:7474",
        auth=('neo4j', '123456')
    )

graph.delete_all()#根据标准名去除重复行
df2=pd.read_csv('标准合2.csv',encoding='gbk',header=0)
df2['标准类型'].fillna(value='未知',inplace=True)
df2['标准性质'].fillna(value='未知',inplace=True)
df2['标准状态_x'].fillna(value='未知',inplace=True)

dpro=df2['标准性质']
dstate=df2['标准状态_x']


dname=df2['标准名']
dunit=df2['起草单位']
dper=df2['起草人']
dcata=df2['标准目录']
dshuyu=df2['标准术语']
dcope=df2['标准范围']
dtype=df2['标准类型']
dbook=df2['相关图书']
drel=df2['相近标准']
print('数据总量为{}'.format(len(dname)))

#为每个文献补充标准号信息
dids=[]
for i in range(len(dname)):
    if df2['基本信息_x'][i]!=None:
        if type(df2['基本信息_x'][i])!=float:
            basicinfo=ast.literal_eval(df2['基本信息_x'][i])
            dids.append(basicinfo[0][1])
        else:
            dids.append(None)
    else:
        dids.append(None)

#为每个文献确定归口单位、主管部门、执行单位、发布单位、标准技术委员会。中文标准分类号、国际标准分类号
#存储形式为list
Gui=[]
Zhu=[]

Zhi=[]
Fa=[]
Biao=[]#str
Zhong=[]#str
Guo=[]#str

for i in range(len(dname)):
    if df2['基本信息_x'][i]!=None and type(df2['基本信息_x'][i])!=float:

            basicinfo=ast.literal_eval(df2['基本信息_x'][i])
            ks=list(basicinfo[i][0] for i in range(len(basicinfo)))
            if '中国标准分类号' in ks:
                ind=ks.index('中国标准分类号')
                Zhong.append(basicinfo[ind][1])
            else:
                Zhong.append(None)
            if '归口单位' in ks:
                ind = ks.index('归口单位')
                Gui.append(basicinfo[ind][1])
            else:
                Gui.append(None)
            if '执行单位' in ks:
                ind = ks.index('执行单位')
                Zhi.append(basicinfo[ind][1])
            else:
                Zhi.append(None)
            if '主管部门' in ks:
                ind = ks.index('主管部门')
                Zhu.append(basicinfo[ind][1])
            else:
                Zhu.append(None)
    else:
            Zhong.append(None)
            Gui.append(None)
            Zhi.append(None)
            Zhu.append(None)


    if df2['基本信息_y'][i]!=None and type(df2['基本信息_y'][i])!=float:
        # if type(df2['基本信息_y'][i])!=float:
            basicinfo = ast.literal_eval(df2['基本信息_y'][i])
            ks = list(basicinfo.keys())
            if '标准技术委员会' in ks:
                Biao.append(basicinfo['标准技术委员会'])
            else:
                Biao.append(None)
            if '发布单位' in ks:
                fu=basicinfo['发布单位'].split(';')
                Fa.append(fu)
            else:Fa.append(None)
            if '国际标准分类号' in ks:
                Guo.append(basicinfo['国际标准分类号'])
            else:
                Guo.append(None)
    else:
            Biao.append(None)
            Fa.append(None)
            Guo.append(None)

matcher=NodeMatcher(graph)
#判断起草人和起草单位，避免重复设立节点
def Judge_Exist(value,relname):
    if value != None:
        if type(value) != float:
            # try:
            dunit_ = ast.literal_eval(value)
            for j in range(len(dunit_)):
                nodelist = list(matcher.match(relname, name=dunit_[j]))
                if len(nodelist) > 0:  # 判断这个节点是否建立过
                    rel_dunit = Relationship(draft, relname, nodelist[0])
                    graph.create(rel_dunit)
                else:
                    unit = Node(relname, name=dunit_[j])
                    graph.create(unit)
                    rel_dunit = Relationship(draft, relname, unit)
                    graph.create(rel_dunit)

def Judge_Exist_list(value,relname):
    if value != None:
        if type(value) != float:
            # try:
            # dunit_ = ast.literal_eval(value)
            dunit_=value
            for j in range(len(dunit_)):
                nodelist = list(matcher.match(relname, name=dunit_[j]))
                if len(nodelist) > 0:  # 判断这个节点是否建立过
                    rel_dunit = Relationship(draft, relname, nodelist[0])
                    graph.create(rel_dunit)
                else:
                    unit = Node(relname, name=dunit_[j])
                    graph.create(unit)
                    rel_dunit = Relationship(draft, relname, unit)
                    graph.create(rel_dunit)

def Judge_Exist_str(value,relname):
    if value != None:
        if type(value) != float:
            # try:
            # dunit_ = ast.literal_eval(value)
            dunit_=value

            nodelist = list(matcher.match(relname, name=dunit_))
            if len(nodelist) > 0:  # 判断这个节点是否建立过
                rel_dunit = Relationship(draft, relname, nodelist[0])
                graph.create(rel_dunit)
            else:
                unit = Node(relname, name=dunit_)
                graph.create(unit)
                rel_dunit = Relationship(draft, relname, unit)
                graph.create(rel_dunit)



def Judge_Existjson(value,relname):
    if value != None:
        if type(value) != float:
            # try:
            ditems = ast.literal_eval(value)
            item_nums=list(ditems.values())
            if len(list(ditems.values()))==3:#匹配相近标准
                for id,name,url in zip(item_nums[0],item_nums[1],item_nums[2]):
                    nodelist = list(matcher.match('标准名', name=name,id=id))
                    if len(nodelist) > 0:  # 判断这个节点是否建立过
                        rel_dunit = Relationship(draft,relname , nodelist[0])
                        graph.create(rel_dunit)
                    else:
                        unit = Node('标准名', name=name,id=id,url=url)
                        graph.create(unit)
                        rel_dunit = Relationship(draft, relname, unit)
                        graph.create(rel_dunit)

            if len(list(ditems.values()))==2:#匹配相关图书
                for name,author in zip(item_nums[0],item_nums[1]):
                    nodelist = list(matcher.match('书籍名', name=name))
                    if len(nodelist) > 0:  # 判断这个节点是否建立过
                        rel_dunit = Relationship(draft,'相关图书' , nodelist[0])
                        graph.create(rel_dunit)
                    else:
                        unit = Node('书籍名', name=name,author=author)
                        graph.create(unit)
                        rel_dunit = Relationship(draft, '相关图书', unit)
                        graph.create(rel_dunit)



#起草单位关系创建
for i in range(0,len(dname)):
    nodelist=list(matcher.match('标准名',name=dname[i],id=dids[i]))
    if len(nodelist)>0:
        draft=nodelist[0]
        matcher=NodeMatcher(graph)
        Judge_Exist(dunit[i],'起草单位')
        Judge_Exist(dper[i],'起草人')
        Judge_Exist(dcata[i], '标准目录')
        Judge_Exist(dshuyu[i], '界定术语')
        Judge_Exist(dcope[i], '标准范围')
        Judge_Existjson(dbook[i], '相关图书')
        Judge_Existjson(drel[i], '相近标准')
        if Gui[i]!=None:
            Judge_Exist_list(Gui[i], "归口单位")
        if Zhu[i]!=None:
            Judge_Exist_list(Zhu[i], '主管部门')
        if Zhi[i]!=None:
            Judge_Exist_list(Zhi[i], '执行单位')
        if Fa[i]!=None:
            Judge_Exist_list(Fa[i], '发布单位')
        if Biao[i]!=None:
            Judge_Exist_str(Biao[i], '标准技术委员会')

    else:
        draft=Node('标准名',
                   name=dname[i],
                   type=dtype[i],
                   property=dpro[i],
                   state=dstate[i],
                   中文标准分类号=Zhong[i],
                   国际标准分类号=Guo[i]
                   )
        graph.create(draft)
        time.sleep(0.2)
        print('创建名为{}的节点'.format(dname[i]))
        matcher = NodeMatcher(graph)
        Judge_Exist(dunit[i],"起草单位")
        Judge_Exist(dper[i],'起草人')
        Judge_Exist(dcata[i],'标准目录')
        Judge_Exist(dshuyu[i],'界定术语')
        Judge_Exist(dcope[i], '标准范围')
        Judge_Existjson(dbook[i],'相关图书')
        Judge_Existjson(drel[i],'相近标准')

        #归口单位、主管部门、分布单位、执行单位、发布单位、标准技术委员会
        if Gui[i] != None:
            Judge_Exist_list(Gui[i], "归口单位")
        if Zhu[i] != None:
            Judge_Exist_list(Zhu[i], '主管部门')

        if Zhi[i] != None:
            Judge_Exist_list(Zhi[i], '执行单位')
        if Fa[i] != None:
            Judge_Exist_list(Fa[i], '发布单位')
        if Biao[i] != None:
            Judge_Exist_str(Biao[i], '标准技术委员会')




