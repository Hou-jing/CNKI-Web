#这是用来下载正在征求意见文献的，注意，webdriver的路径地址发生了改变
#征求意见类PDF可以直接下载

import re
import time
from selenium.webdriver.chrome.options import Options
import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from selenium import webdriver

def Draft_Download(keyword):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        # TODO 增加连接重试次数(一共4次链接)
        sess = requests.Session()
        sess.mount('http://', HTTPAdapter(max_retries=3))
        sess.mount('https://', HTTPAdapter(max_retries=3))
        sess.keep_alive = False  # 关闭多余连接
        base_url = 'http://std.samr.gov.cn/search/std?tid=&q={}'.format(keyword)

        time.sleep(2)

        page_text = requests.get(base_url, headers=headers,  stream=True, verify=False,
                                 timeout=(5, 5))  # connect 和 read 二者的 timeout,所以是一个数组

        # print(page_text.text)
        pattern = 'searchBoxs.*'
        plan_states = re.findall(pattern, page_text.text)
        # print(plan_states)
        pattern2 = r'CURRENT_LINK(.+?)]}'
        obj = re.findall(pattern2, plan_states[0], re.M | re.S | re.I)
        # print(obj)
        page_text.close()
        if '征求意见' in ''.join([i for i in obj]):
            new_base_url = 'http://std.samr.gov.cn/search/stdPage'
            new_params = {
                'q': keyword,
                'tid': '',
                'op': 'CURRENT_LINK:"正在征求意见"'
            }
            time.sleep(1)
            try:
                # TODO 增加连接重试次数(一共4次链接)
                sess = requests.Session()
                sess.mount('http://', HTTPAdapter(max_retries=3))
                sess.mount('https://', HTTPAdapter(max_retries=3))
                sess.keep_alive = False  # 关闭多余连接
                res = requests.get(new_base_url, new_params,headers=headers,  stream=True, verify=False,
                                     timeout=(5, 5))
                tree = etree.HTML(res.text)
                # <a href="http://std.samr.gov.cn/gb/search/gbDetailed?id=E116673ED7B6A3B7E05397BE0A0AC6BF" tid="BV_GB_PLAN" pid="E116673ED7B6A3B7E05397BE0A0AC6BF" target="_blank">
                file_url = tree.xpath('//tr/td[1]/a/@pid')
                print('{}中的征求意见文献数量为{}，文件ID为{}'.format(keyword, len(file_url), file_url))
                time.sleep(2)
                for id in file_url:
                    try:
                        detail_base_url = 'http://std.samr.gov.cn/gb/search/gbDetailed?id={}'.format(id)

                        #更改下载地址
                        options = webdriver.ChromeOptions()
                        out_path = r'E:\python project\pythonProject6.27\graft'  # 是你想指定的路径
                        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
                        options.add_experimental_option('prefs', prefs)
                        #无头界面
                        options.add_argument('--headless')
                        options.add_argument('--disable-gpu')

                        driver = webdriver.Chrome(
                            executable_path='C:\\Program Files\\Google\\Chrome\\Application\\103.0.5060.66\\chromedriver',
                        chrome_options=options)
                        driver.set_page_load_timeout(10)#加载时间
                        driver.get(detail_base_url)
                        time.sleep(3)
                        driver.find_element_by_xpath('//div[3]/div/div/div/div[7]/a[1]').click()
                        time.sleep(5)
                        driver.find_element_by_xpath('//div[3]/div/div/div/div[7]/a[2]').click()
                        driver.close()
                    except Exception as e:
                        print('{}文献没有加载出来'.format(id))
                res.close()
            except Exception as e:
                print('征求意见所有相关的标准文献没有加载出来')
        else:
            print('{}中没有符合要求的标准文献'.format(keyword))

    except Exception as e:
        print(e)


if __name__=='__main__':
    keys=['空间站',
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

    for keyword in keys:
        Draft_Download(keyword)
