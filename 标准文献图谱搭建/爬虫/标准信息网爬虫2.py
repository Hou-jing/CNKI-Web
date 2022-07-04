
#爬取标准文献的基本信息，存储方式csv
#针对的是现行或者国标，对于正在起草文件，标准的属性时不太一样的。
import re
import time

#检索词为微重力时，信息爬取

import pandas as pd
from Cython.Plex import Actions
from requests.adapters import HTTPAdapter
from selenium import webdriver
import ddddocr
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from lxml import etree
from PIL import Image
import ddddocr

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


#网页呈现时，每页大概是10个item


def LookInpaper(detail_base_url):
    driver=webdriver.Chrome(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\102.0.5005.115\\chromedriver')

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






def get_content(file_url,page_id,keyword):
    dict_data = {
        'draft_name': [],
        "label_info": [],
        'label_success': [],
        'label_primary': [],
        'introduction': [],
        'draft_unit': [],
        'draft_person': [],
        'basic_information': [],
        'basic_info_items': [],
        'draft_url': []  # 在线预览界面网址
    }
    for id in file_url:
        try:
            detail_base_url='http://std.samr.gov.cn/gb/search/gbDetailed?id={}'.format(id)
            time.sleep(5)
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
            chrome_options = Options()

            out_path = r'E:\python project\pythonProject6.27\graft_info'  # 是你想指定的路径
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(
                executable_path='C:\\Program Files\\Google\\Chrome\\Application\\103.0.5060.66\\chromedriver',chrome_options=chrome_options)

            time.sleep(10)
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
            print('{}文献已收集'.format(id))
        except Exception as e:
            print('{}连接失败'.format(id))
            DataCsv = pd.DataFrame(dict_data)
            DataCsv.to_csv(keyword + '{}.csv'.format(page_id), mode='w+', encoding='utf_8', index=False)
    DataCsv = pd.DataFrame(dict_data)
    DataCsv.to_csv(keyword + '{}.csv'.format(page_id), mode='w+', encoding='utf_8', index=False)
def Get_Result(keyword):
    base_url = 'http://std.samr.gov.cn/search/stdPage'
    params = {
        'q': keyword,
        'tid': '',
    }

    page_num=0
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        # TODO 增加连接重试次数(一共4次链接)
        sess = requests.Session()
        sess.mount('http://', HTTPAdapter(max_retries=3))
        sess.mount('https://', HTTPAdapter(max_retries=3))
        sess.keep_alive = False  # 关闭多余连接

        page_text = requests.get(base_url, headers=headers, params=params, stream=True, verify=False,
                                 timeout=(5, 5))  # connect 和 read 二者的 timeout,所以是一个数组

        tree = etree.HTML(page_text.text)
        file_nums = tree.xpath('//div[1]/div[1]//text()')
        pattern = r'\d+'

        nums = int(file_nums[1])  # 网页呈现时，每页大概是10个item
        page_num=nums
        print(nums)
        file_url = tree.xpath('//tr/td[1]/a/@pid')
        print(file_url)
        get_content(file_url,page_id=1,keyword=keyword)
        print('第{}页{}抓取完毕，共抓取{}条记录'.format(1, keyword, len(file_url)))

        page_text.close()  # 关闭，很重要,确保不要过多的链接

    except Exception as e:
        print(e)
    pages=page_num//10
    if pages>=2:
        for i in range(2,pages):
        # for i in [2]:
                time.sleep(5)

                base_url = 'http://std.samr.gov.cn/search/stdPage'

                new_params = {
                    'q': keyword,
                    'tid': '',
                    'pageNo' : i
                }
                time.sleep(1.5)

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                }
                # TODO 增加连接重试次数(一共4次链接)
                sess = requests.Session()
                sess.mount('http://', HTTPAdapter(max_retries=3))
                sess.mount('https://', HTTPAdapter(max_retries=3))
                sess.keep_alive = False  # 关闭多余连接
                try:
                    page_text = requests.get(base_url, headers=headers, params=new_params, stream=True, verify=False,
                                             timeout=(5, 5))  # connect 和 read 二者的 timeout,所以是一个数组

                    tree = etree.HTML(page_text.text)
                    file_url = tree.xpath('//tr/td[1]/a/@pid')
                    print(file_url)
                    get_content(file_url,page_id=i,keyword=keyword)
                    print('第{}页{}抓取完毕，共抓取{}条记录'.format(i, keyword, len(file_url)))
                    page_text.close()
                except Exception as e:
                    print('{}抓取出错'.format(i))
    # DataCsv=pd.DataFrame(dict_data)
    # DataCsv.to_csv(keyword+'.csv',mode='w+',encoding='utf_8',index=False)

if __name__=='__main__':
    keys = ['空间站',
            '航天飞机',
            '航天器',
            '有效载荷',
            '空间站科学实验柜',
            '空间应用',
            '空间生命科学与生物技术',
            '空间材料科学',
            '空间天文',
            '空间物理',
            '空间环境',
            '微重力',
            '空间实验',
            '航天实验'
            ]
    for key in keys:
        time.sleep(3)
        Get_Result(key)
