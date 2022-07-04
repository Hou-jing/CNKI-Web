import re
import time

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

#存放标准之间关系的真实网址解析
def Match(page_text):
    import re
    pattern1 = r'<iframe id="framecatalog_YzFiles" .+?/iframe>'
    res = re.findall(pattern1, page_text, re.M | re.S | re.I)
    # print(res)
    pattern_fname = r'filename=(.+?)&'
    fname = re.findall(pattern_fname, res[0], re.M | re.S | re.I)[0]
    # print(fname)
    pattern_val = r'vl=(.+?)"'
    furl = re.findall(pattern_val, res[0], re.M | re.S | re.I)[0]
    # print(furl)
    return fname,furl
#匹配标准之间的关系信息
def MatchRel(page_text):
    # 标准关系的匹配
    rel={
        'refer':[],
        'brefer':[],
        'insti':[],
        'take_':[]
    }
    pattern1 = r'<div class="ebBd">.+?</div>'
    res = re.findall(pattern1, page_text, re.M | re.I | re.S)

    pattern3 = r'[A-Z]{1,3}/?.+?\d{1,8}|[\u4e00-\u9fa5]{1,10}</li>'
    # 引用标准
    refer = re.findall(pattern3, res[0])
    rel['refer'].append(refer)
    # 被引用标准
    brefer = re.findall(pattern3, res[2])
    rel['brefer'].append(brefer)

    # 代替标准
    insti = re.findall(pattern3, res[3])
    rel['insti'].append(insti)
    # 采用标准
    take_ = re.findall(pattern3, res[4])
    rel['take_'].append(take_)
    return rel
#匹配文献基本信息页
def MatchInf(page_text):
    pattern1 = r'<div class="wx-tit">(.+?)</h1>'
    title = re.findall(pattern1, page_text, re.M | re.S | re.I)

    pattern2 = r'<div class="row(.+?)</div>'
    itemlist = re.findall(pattern2, page_text, re.M | re.I | re.S)
    # print(itemlist)
    items = re.findall('span class="row(.+?)</span>', str(itemlist), re.M | re.I | re.S)
    item = re.findall('[\u4e00-\u9fa5]{2,15}', str(items), re.M | re.I | re.S)
    # print(item)
    conlist = re.findall(r'<p.+?</p>', str(itemlist), re.M | re.I | re.S)
    lists = []
    for i in itemlist:
        ele = re.findall(r'<p.+?</p>', i, re.M | re.I | re.S)
        rele = re.findall(r'<p>(.+?)</p>|class="funds">(.+?)</p>', str(ele), re.S | re.M | re.I)
        if rele:
            rele = list(rele[0])
            rele.remove('')
            lists.append(rele)
        else:
            lists.append(None)
    infor_dict = {}
    for i, j in zip(item, lists):
        infor_dict[i] = j

    return infor_dict,title
#捕获文献检索页内容
def Get_Draft_Cont(keyword):
    base_url = 'https://www.cnki.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    # 加表头
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    # browser = webdriver.Chrome(chrome_options=options)
    # 创建一个参数对象，用来控制chrome以无界面模式打开（无头浏览器）
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # 原文链接：https://blog.csdn.net/qq_37195257/article/details/86664297
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    driver = webdriver.Chrome(
        executable_path='C:\\Program Files\\Google\\Chrome\\Application\\103.0.5060.66\\chromedriver',
        chrome_options=options)

    #打开知网标准检索界面，输入关键词
    driver.get(base_url)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="highSearch"]').click()
    time.sleep(5)  # 加载到高级检索页面
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    ele = driver.find_element_by_xpath('//div[3]/div[1]/div/ul[1]/li[8]')
    ActionChains(driver).move_to_element(ele)
    time.sleep(0.5)
    driver.find_element_by_xpath('//div[3]/div[1]/div/ul[1]/li[8]').click()  # /html/body/div[3]/div[1]/div/ul[1]/li[8]
    time.sleep(1)
    ele = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'patentgradetxt')))  # 60s
    driver.find_element_by_xpath('//*[@id="patentgradetxt"]/dd[1]/div[2]/input').send_keys(keyword)
    driver.find_element_by_xpath('//div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/input').click()  # 检索按钮
    draft_dict = {}
    # 文献基本信息储存字典
    keys = ['title','basic', 'patent', 'technological', 'relations', 'dynamic', 'relation_books']
    for k in keys:
        draft_dict[k] = []
    try:
        ele_ = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-table-list')))  # 60s

        draft_nums = driver.find_element_by_xpath('//*[@id="countPageDiv"]/span').text
        print('{}{}'.format(keyword,draft_nums))#获取文献检索总数目
        res = re.findall('\d+', str(draft_nums), re.M | re.I | re.S)

        # 捕获文献基本信息，设定条件是文献检索数量在50篇以下
        if True:
            ele__ = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'result-table-list')))  # 60s

            if ele__ and int(res[0])<50:
                for i in range(1,int(res[0])+1):
                    time.sleep(5)
                    if i==1:
                        driver.find_element_by_xpath('//*[@id="gridTable"]/table/tbody/tr/td[2]/a').click()
                    if i!=1:
                        driver.switch_to.window(driver.window_handles[1])
                        driver.find_element_by_xpath('//*[@id="gridTable"]/table/tbody/tr[{}]/td[2]/a'.format(i)).click()
                    try:

                        driver.switch_to.window(driver.window_handles[-1])
                        try:
                            #基本信息
                            print('开始爬取第{}条'.format(i))
                            infor_dict,title=MatchInf(driver.page_source)
                            draft_dict['basic'].append(infor_dict)
                            draft_dict['title'].append(title)
                            js = "var q=document.documentElement.scrollTop=100000"
                            driver.execute_script(js)
                            time.sleep(3)
                            relation_books = driver.find_element_by_xpath('//*[@id="dz-carousel"]/div/div[1]/div[2]').text
                            draft_dict['relation_books'].append(relation_books)
                            fname,val_=Match(driver.page_source)
                            time.sleep(1)

                            basic_url = 'https://kns.cnki.net/kcms/detail/frame/list.aspx'
                            params_patent = {
                                'filename': fname,
                                'dbcode': 'SCSF',
                                'dbname': 'SCSF',
                                'reftype': '3',
                                'vl': val_
                            }
                            sess = requests.Session()
                            sess.mount('http://', HTTPAdapter(max_retries=3))
                            sess.mount('https://', HTTPAdapter(max_retries=3))
                            sess.keep_alive = False  # 关闭多余连接
                            try:
                                requests.packages.urllib3.disable_warnings()
                                pat = requests.get(basic_url, headers=headers, params=params_patent, stream=True,
                                                   verify=False,
                                                   timeout=(5, 5))  # connect 和 read 二者的 timeout,所以是一个数组
                                relat = pat.text
                                rel = MatchRel(relat)
                                draft_dict['relations'].append(rel)
                            except:
                                draft_dict['relations'].append(None)
                            #专利发明

                            patent=driver.find_element_by_link_text('专利发明')
                            ActionChains(driver).move_to_element(patent).click()
                            try:
                                patents=driver.find_element_by_xpath('//h3').text
                            except:
                                patents=driver.find_element_by_xpath('//div/div/div/div[2]').text
                            draft_dict['patent'].append(patents)
                            # print('专利',patents)
                            #科技成果
                            time.sleep(1)
                            tech_achieve = driver.find_element_by_link_text('科技成果')
                            ActionChains(driver).move_to_element(tech_achieve).click()
                            try:
                                patents = driver.find_element_by_xpath('//h3').text
                            except:
                                patents=driver.find_element_by_xpath('//div/div/div/div[2]').text

                            draft_dict['technological'].append(patents)
                            time.sleep(1)
                            #核心技术动态

                            tech=driver.find_element_by_link_text('所涉核心技术研究动态')
                            ActionChains(driver).move_to_element(tech).click()
                            try:
                                ele = driver.find_element_by_xpath('//h3').text
                            except:
                                ele = driver.find_element_by_xpath('//div/div/div/div[2]').text
                            draft_dict['dynamic'].append(patents)
                            #标准之间的关系

                            # driver.close()
                            print('{}中第{}条文献信息获取完成'.format(keyword,i))
                        except Exception as e:
                            print('{}中第{}条文献信息没有加载出来'.format(keyword,i))

                    except Exception as e:
                        print('{}相关的文献没有检索到'.format(keyword))
            elif int(res[0])>50:
                for i in range(1,51):
                    time.sleep(5)
                    if i==1:
                        driver.find_element_by_xpath('//*[@id="gridTable"]/table/tbody/tr/td[2]/a').click()
                    if i!=1:
                        driver.switch_to.window(driver.window_handles[1])
                        driver.find_element_by_xpath('//*[@id="gridTable"]/table/tbody/tr[{}]/td[2]/a'.format(i)).click()
                    try:

                        driver.switch_to.window(driver.window_handles[-1])
                        try:
                            #基本信息
                            print('开始爬取第{}条'.format(i))
                            infor_dict,title=MatchInf(driver.page_source)
                            draft_dict['basic'].append(infor_dict)
                            draft_dict['title'].append(title)
                            js = "var q=document.documentElement.scrollTop=100000"
                            driver.execute_script(js)
                            time.sleep(3)
                            relation_books = driver.find_element_by_xpath('//*[@id="dz-carousel"]/div/div[1]/div[2]').text
                            draft_dict['relation_books'].append(relation_books)
                            fname,val_=Match(driver.page_source)
                            time.sleep(1)
                            basic_url = 'https://kns.cnki.net/kcms/detail/frame/list.aspx'
                            params_patent = {
                                'filename': fname,
                                'dbcode': 'SCSF',
                                'dbname': 'SCSF',
                                'reftype': '3',
                                'vl': val_
                            }
                            sess = requests.Session()
                            sess.mount('http://', HTTPAdapter(max_retries=3))
                            sess.mount('https://', HTTPAdapter(max_retries=3))
                            sess.keep_alive = False  # 关闭多余连接
                            try:

                                requests.packages.urllib3.disable_warnings()
                                pat = requests.get(basic_url, headers=headers, params=params_patent, stream=True,
                                                   verify=False,
                                                   timeout=(5, 5))  # connect 和 read 二者的 timeout,所以是一个数组
                                relat = pat.text
                                rel = MatchRel(relat)
                                draft_dict['relations'].append(rel)
                            except:
                                draft_dict['relations'].append(None)


                            #专利发明
                            patent=driver.find_element_by_link_text('专利发明')
                            ActionChains(driver).move_to_element(patent).click()
                            try:
                                patents=driver.find_element_by_xpath('//h3').text
                            except:
                                patents=driver.find_element_by_xpath('//div/div/div/div[2]').text
                            draft_dict['patent'].append(patents)
                            # print('专利',patents)
                            #科技成果
                            time.sleep(1)
                            tech_achieve = driver.find_element_by_link_text('科技成果')
                            ActionChains(driver).move_to_element(tech_achieve).click()
                            try:
                                patents = driver.find_element_by_xpath('//h3').text
                            except:
                                patents=driver.find_element_by_xpath('//div/div/div/div[2]').text

                            draft_dict['technological'].append(patents)
                            time.sleep(1)
                            #核心技术动态
                            tech=driver.find_element_by_link_text('核心技术动态')
                            ActionChains(driver).move_to_element(tech).click()
                            try:
                                ele = driver.find_element_by_xpath('//h3').text
                            except:
                                ele = driver.find_element_by_xpath('//div/div/div/div[2]').text
                            draft_dict['dynamic'].append(patents)
                            #标准之间的关系

                            # driver.close()
                            print('{}中第{}条文献信息获取完成'.format(keyword,i))
                        except Exception as e:
                            print('{}中第{}条文献信息没有加载出来'.format(keyword,i))

                    except Exception as e:
                        print('{}相关的文献没有检索到'.format(keyword))
                print('{}文献总量超过了50'.format(keyword))
            else:
                print('{}文献没有加载出来'.format(keyword))
        # aqy7hLTGoBQZgrxgmPn-OYOxZCezuVdvc_VXii2wDi1n7yiMsNHIIt4CW0DgaWXL
    except Exception as e:
        print('{}没有检索到文献信息'.format(keyword))
    driver.close()
    Draft_Data = pd.DataFrame.from_dict(draft_dict, orient='index')
    Draft_Data = Draft_Data.T
    Draft_Data.to_csv(keyword + '.csv', encoding='utf_8', mode='w+', index=False)
if __name__=='__main__':
    keyword = [
        '空间站',
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
    for draftkey in keyword:
        time.sleep(5)
        Get_Draft_Cont(draftkey)
        print('{}文献抓取完成'.format(draftkey))
