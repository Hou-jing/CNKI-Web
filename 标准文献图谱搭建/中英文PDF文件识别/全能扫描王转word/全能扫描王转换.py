import re
import sys, fitz
import os
import datetime,time
#在线文字识别
import os
import re
import time
import pyperclip
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

# 一直等待某元素可见，默认超时10秒
def is_visible(driver,locator, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

'''————————————————
版权声明：本文为CSDN博主「angel725」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/angel725/article/details/113781994'''
def Get_singlepdf(fpath):#识别单张图片的内容
    #无头浏览器
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    #
    # driver = webdriver.Chrome(
    #     executable_path='C:\\Program Files\\Google\Chrome\\Application\\104.0.5112.79\\chromedriver',
    #     chrome_options=options)
    driver = webdriver.Chrome(
        executable_path='C:\\Program Files\\Google\Chrome\\Application\\104.0.5112.79\\chromedriver')
    url='https://www.camscanner.com/pdftoword'
    driver.get(url)
    # fpath='E:\\python project\\pythonProject6.27\\标准PDF转化\\扫描件图片\\GBT 28874-2012 空间科学实验数据产品分级规范\\images_3.png'
    driver.find_element_by_xpath("//input[@type='file']").send_keys(fpath)
    time.sleep(5)
    if is_visible(driver,'//*[@id="app"]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div'):
        driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div').click()#触发复制
        time.sleep(5)
        print('{}转换成功'.format(fpath.split('\\')[-1]))

#识别一个文件夹下的所有的标准文件
def Get_fils(dir):
    file_lists=os.listdir(dir)
    pdf_nums=0
    for file in file_lists:
        if 'pdf' in file:
            pdf_nums+=1
            Get_singlepdf(dir + '\\' + file)

            
    print('标准数量总数为{}'.format(pdf_nums))

dir='E:\\python project\\pythonProject6.27\\标准PDF转化\\全能扫描王转word'
Get_fils(dir)
