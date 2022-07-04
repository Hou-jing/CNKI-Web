import os
import shutil

base_path='E:\python project\pythonProject6.27\标准知识图谱\文献爬虫'
new_path='E:\python project\pythonProject6.27\标准知识图谱\文献内容清洗\ori_file'

#文献移动到ori_file文件夹内
for fname in os.listdir(base_path):
    if '.csv' in fname:
        old_path=os.path.join(base_path,fname)
        shutil.move(old_path,new_path)#旧文件目录，新文件目录
        print('{}移动成功'.format(fname))


zhiw_path='E:\python project\pythonProject6.27\标准知识图谱\文献爬虫\知网爬虫'
for fname in os.listdir(base_path):
    if '.csv' in fname:
        old_path=os.path.join(zhiw_path,fname)
        shutil.move(old_path,new_path)#旧文件目录，新文件目录
        print('{}移动成功'.format(fname))
