import os

import docx

from docx import Document

def File2text(fpath):
    doc = Document(fpath)
    newfpath=open(fpath.replace('.docx','.txt'),mode='w+',encoding='utf_8')
    for paragraph in doc.paragraphs:
        # print(paragraph.text)
        newfpath.write(paragraph.text)
        newfpath.write('\n')
    print('{}转换成功'.format(fpath.split('\\')[-1]))

dir='E:\\python project\\pythonProject6.27\\标准PDF转化\\word转text'
for file in os.listdir(dir):
    if 'docx' in file:
        File2text(dir+'\\'+file)