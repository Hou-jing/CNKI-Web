# coding:utf-8
#将标准信息网下爬取的所有文件合并到一个csv文件中
import pandas as pd
import os

# Folder_Path='E:\python project\pythonProject6.27\标准知识图谱\文献内容清洗\ori_file\infornet'
# SaveFile_Name = r'E:\python project\pythonProject6.27\标准知识图谱\文献内容清洗\all.csv'  # 合并后要保存的文件名
Folder_Path='E:\python project\pythonProject6.27\标准知识图谱\文献爬虫\知网爬虫'
SaveFile_Name = r'E:\python project\pythonProject6.27\标准知识图谱\文献内容清洗\zhi.csv'  # 合并后要保存的文件名
# 修改当前工作目录
os.chdir(Folder_Path)
# 将该文件夹下的所有文件名存入一个列表
file_list = os.listdir()
file_first=''
n=0
for i in file_list:
    n+=1
    if '.csv' in i:
        file_first=i
        break
# 读取第一个CSV文件并包含表头
df = pd.read_csv(Folder_Path + '\\' + file_first)  # 编码默认UTF-8，若乱码自行更改

# 将读取的第一个CSV文件写入合并后的文件保存
df.to_csv(SaveFile_Name, encoding="gbk", index=False)

# 循环遍历列表中各个CSV文件名，并追加到合并后的文件
for i in range(n, len(file_list)):
    if '.csv' in file_list[i]:
        try:
            df = pd.read_csv(Folder_Path + '\\' + file_list[i])
            df.to_csv( SaveFile_Name, encoding="gbk", index=False, header=False, mode='a+')
        except:
            print('第{}个文件出错'.format(i))
    else:
        continue

