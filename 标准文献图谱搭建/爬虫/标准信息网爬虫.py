#爬取标准文献的基本信息，存储方式csv
import re
import time

#检索词为微重力时，信息爬取

import pandas as pd
from Cython.Plex import Actions
from selenium import webdriver
import ddddocr
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from lxml import etree
from PIL import Image
import ddddocr

base_url='http://std.samr.gov.cn/search/stdPage'
keyword='微重力'
params={
    'q':keyword,
    'tid':'',
}
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
time.sleep(1)
page_text=requests.get(base_url,params=params,headers=headers).text

# print(page_text)
tree = etree.HTML(page_text)
#http://std.samr.gov.cn/search/stdPage?q=%E5%BE%AE%E9%87%8D%E5%8A%9B&tid=0

#原地址：般来说一个中文字对应三个%编码的是utf-8, 一个中文字对应两个%编码的是GB2312。
#http://std.samr.gov.cn/search/std?tid=&q=%E5%BE%AE%E9%87%8D%E5%8A%9B
file_url=tree.xpath('//tr/td[1]/a/@pid')
# print(file_url)
#标准详情界面
# <a href="http://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D7F3B3D3A7E05397BE0A0AB82A" tid="BV_GB" pid="71F772D7F3B3D3A7E05397BE0A0AB82A" target="_blank"><span class="en-code">GB/T 30114.7-2014</span>&nbsp;&nbsp;空间科学及其应用术语  第7部分：<sacinfo>微重力</sacinfo>科学</a>

def LookInpaper(detail_base_url):
    # driver=webdriver.Chrome(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\102.0.5005.115\\chromedriver')

    get_html = "test.html"
    # 打开文件，准备写入
    f = open(get_html, 'wb')
    driver.get(detail_base_url)
    time.sleep(2)  # 保证浏览器响应成功后再进行下一步操作
    # 写入文件
    f.write(driver.page_source.encode("utf-8", "ignore"))  # 忽略非法字符
    print('写入成功')
    # 关闭文件
    f.close()
    page_text = open('test.html', encoding='utf_8', mode='r+').read()
    pattern2 = r'\.openpdf(.+?)window\.open(.+?)}\)'
    searchObj2 = re.search(pattern2, page_text, re.M | re.S)
    # print(searchObj2.group())
    print(searchObj2.group(2))
    # print(searchObj2.group(1))
    pattern3 = r"http(.*)\',"
    new_text = searchObj2.group(2)
    searchObj3 = re.search(pattern3, new_text)
    print(searchObj3.group(1))
    new_url = 'http' + searchObj3.group(1)#得到在线预览的网址
    driver.get(new_url)

    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//div[2]/div/div/div/div/table[2]/tbody/tr[4]/td/button[1]').click()
    driver.switch_to.window(driver.window_handles[-1])
    img_id = driver.find_element_by_xpath('//*[@id="myModal"]/div/div/div[2]/img')
    img_id = img_id.get_attribute('src')
    img_base_url = 'http://c.gb688.cn/bzgk/gb/gc?{}'.format(img_id)
    js = "window.open('{}','_blank');"
    driver.execute_script(js.format('http://web2.com'))
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(img_base_url)
    img_ = driver.get_screenshot_as_png()
    f = open('抓取1.png', 'wb')
    f.write(img_)
    cropped = Image.open("抓取1.png").crop((530, 380, 750, 500))  # (left, upper, right, lower)
    cropped.save('code.png')
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(open('code.png', 'rb').read())
    print(res)
    driver.switch_to.window(driver.window_handles[-2])
    driver.find_element_by_xpath('//*[@id="verifyCode"]').send_keys(res)
    driver.find_element_by_xpath('//*[@id="myModal"]/div/div/div[3]/button').click()
    time.sleep(3)

dict_data={
    'draft_name':[],
    "label_info":[],
'label_success':[],
'label_primary':[],
'introduction':[],
'draft_unit':[],
'draft_person':[],
'basic_information':[],
'basic_info_items':[],
     'draft_url':[]#在线预览界面网址
     }
#标准基本信息
def Type(content):
    if type(content) == str:
        item = content.replace('\n', '').replace('\t', '')
        return item
    elif type(content == list):
        if content != ['']:
            item = [i.replace('\n', '').replace('\t', '') for i in content]

            return item
def get_basic_infor(page_source):
    pattern=r'basicInfo-item.*?>(.+?)<'
    search_obj=re.findall(pattern,page_source,re.M|re.I|re.S)
    basic_items=[]
    for i in range(len(search_obj)):
        pattern=r'<.*?>(.*)'
        text=search_obj[i]
        search_res=re.findall(pattern,text)
        if search_res:
            search_obj[i]=search_res
    for i in range(0,len(search_obj),2):
        if i+1<len(search_obj):
            item_=Type(search_obj[i])
            item__=Type(search_obj[i+1])
            if item__!=None and item_!=None:
                basic_items.append((item_,item__))
    return basic_items

#相近标准
def get_draft_near(page_source):
    pattern = r'<dd class="basicInfo-item value".*?<a href=(.+?)</a></dd>'
    search_obj = re.findall(pattern, page_source, re.M | re.I | re.S)
    # print(search_obj)
    links = []  # 标准对应的链接
    draft_ids = []  # 标准号
    draft_names = []  # 标准名
    for i in range(len(search_obj)):
        pattern = r'http.+?"'
        text = search_obj[i]
        link = re.findall(pattern, text)[0]
        links.append(link.replace('"', '').replace("'", "").replace('\n', ''))
        pattern2 = r'/span>(.+?)&nbsp'
        draft_id = re.findall(pattern2, text)[0]
        draft_ids.append(draft_id)
        pattern3 = r'&nbsp;(.*)'
        draft_name = re.findall(pattern3, text)
        draft_names.append(draft_name)
    return links, draft_ids, draft_names

for id in file_url:
    detail_base_url='http://std.samr.gov.cn/gb/search/gbDetailed?id={}'.format(id)
    time.sleep(1)
    deres=requests.get(detail_base_url,headers=headers).text
    # print(deres)
    detree=etree.HTML(deres)
    draft_name=detree.xpath('//div[3]/div/div/div/div[1]/h4/text()')
    label_info=detree.xpath('//div[3]/div/div/div/div[1]/div/span[1]/text()')#国家标准or。。#返回列表类型
    label_success=detree.xpath('//div[3]/div/div/div/div[1]/div/span[2]/text()')#推荐性or..
    label_primary=detree.xpath('//div[3]/div/div/div/div[1]/div/span[3]/text()')#现行or..
    intro=detree.xpath('//div[3]/div/div/div/p[1]//text()')#第一段
    draft_unit=detree.xpath('//div[3]/div/div/div/p[2]//text()')#起草单位
    draft_per=detree.xpath('//div[3]/div/div/div/p[3]//text()')#起草人


    # #查看全文
    # LookInpaper(detail_base_url)
    ##http://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=5C75B7A54C1037F2107B4ADF5EA3E41C
    driver = webdriver.Chrome(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\102.0.5005.115\\chromedriver')
    time.sleep(2)
    driver.get(detail_base_url)
    pattern2 = r'\.openpdf(.+?)window\.open(.+?)}\)'
    searchObj2 = re.search(pattern2,  driver.page_source, re.M | re.S)
    pattern3 = r"http(.*)\',"
    new_text = searchObj2.group(2)
    searchObj3 = re.search(pattern3, new_text)
    # print(searchObj3.group(1))
    new_url = 'http' + searchObj3.group(1)  # 得到在线预览的网址
    basic_infor = get_basic_infor(driver.page_source)#基本信息
    links, draft_ids, draft_names=get_draft_near(driver.page_source)#相近标准
    driver.close()
    dict_data['draft_name'].append(draft_name),dict_data['label_info'].append(label_info),dict_data['label_success'].append(label_success),dict_data['label_primary'].append(label_primary),
    dict_data['introduction'].append(intro),dict_data['draft_unit'].append(draft_unit),dict_data['draft_person'].append(draft_per),
    dict_data['basic_information'].append(basic_infor),dict_data['basic_info_items'].append((links,draft_ids,draft_names)),dict_data['draft_url'].append(new_url)
DataCsv=pd.DataFrame(dict_data)
DataCsv.to_csv(keyword+'.csv',mode='w+',encoding='utf_8',index=False)
print('{}抓取完毕，共抓取{}条记录'.format(keyword,len(file_url)))




