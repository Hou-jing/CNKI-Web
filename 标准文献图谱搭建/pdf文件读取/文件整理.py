#文件整理，删除重复文件
import os

flist=os.listdir('E:\\python project\\pythonProject6.27\\graft')
dir='E:\\python project\\pythonProject6.27\\graft'
for fname in flist:
    str_del = "(1)"
    if str_del in fname:
        os.remove(os.path.join(dir,fname))
