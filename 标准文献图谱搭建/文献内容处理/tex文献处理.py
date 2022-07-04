import os
import re

import pandas as pd

draft_dict={
    'file_name':[],
    'english_name':[],#英文名
    'chinese_name':[],#中文名
    'graft_type':[],#标准类型（征求意见）
'graft_catalogs':[],#标准目录
    'scope':[],#标准范围
    'refer_res':[],#规范性引用文件
'onym_res':[],#术语和定义
'num_res':[]#章节内容
}
# fpath='20_WD_2020102799_空间环境 宇航用半导体器件在轨单粒子事件.txt'
def Get_Content(fpath):
    draft_dict['file_name'].append(fpath)
    f=open(fpath,encoding='utf_8',mode='r+').readlines()
    # print(f)
    content='\n'.join([i.replace('\n','').replace('\t','').replace('.','') for i in f])
    # print(content)

    pattern1=r'[a-z,A-Z](.+?)目.*录'#获取封面内容
    obj_cover=re.findall(pattern1,content,re.I|re.M|re.S)
    if obj_cover:
        name=obj_cover[0].replace('\n','')
        # print(obj_cover[0].replace('\n',''))
        pattern2=r'[a-z,A-Z]{2,}'#匹配外文字符
        eng=' '.join(re.findall(pattern2,name)).replace('XXXX','')
        # print('english_name',eng)
        pattern3=r'[\u4e00-\u9fa5]+'#匹配中文字符
        chinese_name=str(re.findall(pattern3,name))
        graft_type=str(re.findall(pattern3,name))
        # print('chinese_name',chinese_name)
        # print('graft_type',graft_type)
        if eng:
            draft_dict['english_name'].append(eng)
        else:
            draft_dict['english_name'].append('-')
        if chinese_name:
            draft_dict['chinese_name'].append(chinese_name)
        else:
            draft_dict['chinese_name'].append('-')
        if graft_type:
            draft_dict['graft_type'].append(graft_type)
        else:
            draft_dict['graft_type'].append('-')




    #文件目录
    pattern4=r'\d\s+([\u4e00-\u9fa5]+)'
    cata=re.findall('目\s+录(.*?)前\s+言|目\s+次(.*?)前\s+言',content,re.M|re.S|re.I)

    if cata:
        catalog=re.findall(pattern4,str(cata),re.I|re.S|re.M)
        if catalog:
            # print('graft_catalogs',catalog)
            draft_dict['graft_catalogs'].append(catalog)
    else:
        draft_dict['graft_catalogs'].append('-')
    main_body=re.findall('前\s*?言\s+[\u4e00-\u9fa5]{1,}.*',content,re.M|re.I|re.S)[0]
    #获取范围（前言在基本信息中已经包括，就不在单独分析

    pattern5=r'范\s*?围(.+?)。\s+2\s*'
    scope=''.join(re.findall(pattern5,main_body,re.M|re.I|re.S)).replace('\n','').replace('\t','').replace('2','')
    # print('cata',scope)
    draft_dict['scope'].append(scope) if scope else draft_dict['scope'].append('-')
    #规范性引用文件（可选规范性要素）
    #规范性引用文件（因为不是必备要素，目录也不是必备要素，不能从目录判断该元素是否存在）
    pattern_refer_exist=r'(\d+)\s*规范性引用文件'
    refer_res=re.findall(pattern_refer_exist,content,re.M|re.I|re.S)
    if refer_res:
        chapter_num=int(refer_res[0])
        next_chap_num=chapter_num+1
        # 定位规范性引用文件文字块
        pattern_ref=r'(%s)\s*规范性(.+?)(%s)\s'%(chapter_num,next_chap_num)
        refer=re.findall(pattern_ref,main_body,re.M|re.S|re.I)[0]
        # print('refer',refer)
        #定义具体条款
        pattern6=r'[a-z,A-Z]+.*'
        refer_docu=re.findall(pattern6,''.join([i for i in refer]),re.I)
        # print('Reference documents',refer_docu)
        draft_dict['refer_res'].append(refer_docu) if refer_docu else draft_dict['refer_res'].append('-')
    else:
        draft_dict['refer_res'].append('-')
    #术语和定义（可选规范性要素）
    pattern_onym_exist=r'(\d+)\s*术语和定义'
    onym_res=re.findall(pattern_onym_exist,content,re.M|re.I|re.S)
    # print(onym_res)
    if onym_res:
        #定义术语文字块
        chapter_num = int(onym_res[0])
        next_chap_num = chapter_num + 1
        pattern_onym = r'(%s)\s*术语和(.+?)(%s)\s?[\u4e00-\u9fa5]{1,}' % (chapter_num, next_chap_num)
        onyms =re.findall(pattern_onym,main_body,re.M|re.S|re.I)
        # print('onyms',onyms)
        if onyms:
            pattern_items=r'[\u4e00-\u9fa5]{1,}\s+?[a-z,A-Z]+.+?。'
            term_lists=re.findall(pattern_items,str(onyms).replace('\n','').replace('\\n',''),re.S|re.M|re.I)
            # print('term_list',term_lists)
            draft_dict['onym_res'].append(term_lists) if term_lists else draft_dict['onym_res'].append('-')
        else:
            draft_dict['onym_res'].append('-')
    else:
        draft_dict['onym_res'].append('-')
    #获取整个文献最大章节数
    nums_pattern=r'\d\d?\s+'
    num_res=re.findall(nums_pattern,main_body,re.M|re.S|re.I)
    # print(num_res)
    content={}#章节内容存放在字典中
    if num_res:
        nums=int(num_res[-1].replace('\n','').replace(' ',''))
        total_nums=10
        if nums in list(range(15)):
            total_nums=nums
        else:
            total_num=10#假设只有10章
        begin_num=2
        if refer_res:
            n1 = int(refer_res[0])
            if n1 > begin_num:
                begin_num = n1
        if onym_res:
            n2 = int(onym_res[0])
            if n2 > begin_num:
                begin_num = n2

        # print('begin num', begin_num)
        for chapter in range(begin_num + 1, total_nums):
            pattern_chap = r'^(%s)\d?\s*[\u4e00-\u9fa5]{0,8}(.+?)(%s)\s+[\u4e00-\u9fa5]{1,15}\s?$' % (
                chapter, chapter + 1)
            chapter_res = re.findall(pattern_chap, main_body, re.M | re.S | re.I)
            if chapter_res:
                content[chapter] = chapter_res
        # print('total num', total_nums)
        chapter = total_nums
        pattern_last_chap = r'^(%s)\d?\s*[\u4e00-\u9fa5]{0,8}.*$' % chapter
        chapter_res = re.findall(pattern_last_chap, main_body, re.M | re.S | re.I)
        if chapter_res:
            content[chapter] = chapter_res

    # print(content)
    draft_dict['num_res'].append(content)

if __name__=='__main__':
    dir='E:\\python project\\pythonProject6.27\\graft'
    flist=os.listdir(dir)
    for fname in flist:
        if '.txt' in fname:
            path=os.path.join(dir,fname)
            Get_Content(fpath=path)
            print('{}文献内容分析完成'.format(fname))

    Draft_content=pd.DataFrame.from_dict(draft_dict,orient='index')#orient='index'可以解决array长度不等的问题
    Draft_content=Draft_content.T
    Draft_content.to_csv('征求意见类.csv',encoding='utf-8-sig',mode='w+',index=False)

#数据还是有些脏、需要进一步处理。









