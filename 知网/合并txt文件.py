import os
base_path='E:\\=复杂网络\\知网2\\'
file_dir=os.listdir(base_path)
f=open('CNKI2.txt', 'w', encoding='utf_8')
test_li=['AB','SN','CN','LA','DS','IS','RT','SR','A1','AD','T1','JF', 'YR','IS','vo','OP','K1']

for file_name in file_dir:
    i=0
    for line in open(base_path+file_name, encoding='utf_8'):
        if line in ['\n']:
            f.write('\n')
            i+=1
        else:
            test=line.split(' ')[0]
            if test in test_li:
                f.write(line)

    print('空行数为{}'.format(i))
f.close()
#import os
# f=open('CNKI.txt', 'w', encoding='utf_8')
# test_li=['AB','SN','CN','LA','DS','IS','RT','SR','A1','AD','T1','JF', 'YR','IS','vo','OP','K1']
# import os
# print(os.listdir())
# for line in open('D:/PycharmProjects/pythonProject1/爬虫/文件操作/数据分析基础/CNKI 关键词处理/测试.txt',encoding='utf_8'):
#     if line in ['\n']:
#         print('T')
#         f.write('\n')
#     else:
#         test=line.split(' ')[0]
#         if test in test_li:
#             f.write(line)
# f.close()