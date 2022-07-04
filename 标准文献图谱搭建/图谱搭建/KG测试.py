import os
import pandas as pd
import re
from py2neo import Graph, Node, Relationship
#查看数据基本信息
df=pd.read_csv('new_参考文献.csv',encoding='gbk')
# print(df.info)
print(df.describe())
#查看列中是否有空缺值
temp = df.isnull().any() #列中是否存在空值
print(type(temp))
print(temp)

def creat_node(file,graph):
    if not os.path.exists(file):
        print('{} 文件不存在'.format(file))
    df=pd.read_csv(file,encoding='gbk')
    df = df.fillna(value=str('相关信息不存在'))
    # for column in list(df.columns)[:]:
    #     a = df[column]
    #     for i in zip(a):
    #         #print(i)
    #         reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    #         i = re.sub(reg, '', str(i))
    #         #print(i)
    #         node = Node(column,name=i)
    #         if not graph.find_one(label=column, property_key='name', property_value=i):
    #             graph.create(node)
    #             print('创建了新 结点 ： {}'.format(node))
    draft_cname,draft_ename=df['标准名'],df['英文名']
    draft_state=df['标准状态']
    draft_cata=df['标准目录']
    draft_scope=df['标准范围']
    # name,shortname = df.name,df.shortname
    # province,city =  df.province,df.city
    # manager,chairman = df.manager,df.chairman

    for cname,ename,state,cata,scope in zip(draft_cname,draft_ename,draft_state,draft_cata,draft_scope):
        name_node=Node('标准名',
                       name=cname,
                       english_name=ename,
                       states=state,
                       catalog=cata
                       )
        scope_node = Node('标准范围',
                       name=scope,
                       )

        # if not graph.find_one(label='名字',property_key='name',property_value=name):
        if not  graph.nodes.match('标准名',cname).first():
            graph.create(name_node)
        # if not graph.find_one(label='所在地',property_key='name',property_value=province):
        if not  graph.nodes.match('标准范围',scope).first():
            graph.create(scope_node)

        relationship1 = Relationship(name_node, '标准适用范围', scope_node)
        graph.create(relationship1)
        # print('标准范围关系已建立')

if __name__=='__main__':
    #graph = Graph(password="")
    graph = Graph(
        "http://localhost:7474",
        auth=('neo4j', '123456')
    )
    graph.delete_all()
    chess_file = 'new_参考文献.csv'
    creat_node(chess_file,graph)
