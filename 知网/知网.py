import time
from selenium.webdriver.common.action_chains import ActionChains
import selenium
from selenium import webdriver
#import tesserocr#识别图片验证码
from  selenium.webdriver.common.keys import Keys
webdriver=webdriver.Chrome('C:\\Program Files (x86)\\Google\\Update\\1.3.36.112\\chromedriver.exe')
webdriver.get('https://kns.cnki.net/kns8/AdvSearch?dbprefix=SCDB&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCJD%2CCCVD%2CCJFN')
webdriver.find_element_by_xpath('//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys('复杂网络',Keys.ENTER)

element=webdriver.find_element_by_xpath('/html/body/div[3]/div[1]/div/ul[1]/li[1]/a')
webdriver.execute_script('arguments[0].click()',element)
time.sleep(5)
botton=webdriver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/a[2]')
webdriver.execute_script('arguments[0].click()',botton)
time.sleep(5)
webdriver.execute_script('arguments[0].click()',webdriver.find_element_by_xpath('//*[@id="JournalSourceType"]/label[2]'))
webdriver.find_element_by_xpath('//*[@id="JournalSourceType"]/label[3]/input').click()
webdriver.find_element_by_xpath('//*[@id="JournalSourceType"]/label[4]/input').click()
webdriver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input').click()
time.sleep(1)
webdriver.find_element_by_xpath('//*[@id="perPageDiv"]/div').click()
element=webdriver.find_element_by_xpath('//*[@id="perPageDiv"]/ul/li[3]/a')
ActionChains(webdriver).move_to_element(element).click().perform()
def get_text():
    i = 1
    while i % 11 != 0:
        time.sleep(1)
        try:
            webdriver.find_element_by_xpath('//*[@id="changeVercode"]')#验证码
            webdriver.find_element_by_xpath('//*[@id="vericode"]').send_keys('')
            element=webdriver.find_element_by_xpath('//*[@id="checkCodeBtn"]')
            ActionChains(webdriver).move_to_element(element).click().perform()
            time.sleep(1)
            webdriver.find_element_by_xpath('//*[@id="selectCheckAll1"]').click()
            time.sleep(0.5)
            webdriver.find_element_by_xpath('//*[@id="Page_next_top"]').click()
            time.sleep(0.5)
        except:
            webdriver.find_element_by_xpath('//*[@id="selectCheckAll1"]').click()
            time.sleep(0.5)
            webdriver.find_element_by_xpath('//*[@id="Page_next_top"]').click()
            time.sleep(0.5)
        print('已勾选', i * 50)
        i += 1


    element=webdriver.find_element_by_xpath('//*[@id="batchOpsBox"]/li[2]/a')#文献分析
    ActionChains(webdriver).move_to_element(element).perform()
    element=webdriver.find_element_by_xpath('//*[@id="batchOpsBox"]/li[2]/ul/li[1]/a')#导出分析
    ActionChains(webdriver).move_to_element(element).perform()
    element=webdriver.find_element_by_xpath('//*[@id="batchOpsBox"]/li[2]/ul/li[1]/ul/li[8]/a')#refwork
    ActionChains(webdriver).move_to_element(element).click().perform()
    # webdriver.find_element_by_xpath('//*[@id="batchOpsBox"]/li[2]/ul/li[1]/ul/li[8]/a').click()
    # webdriver.execute_script('argument[0].click()',webdriver.find_element_by_xpath('//*[@id="batchOpsBox"]/li[2]/ul/li[1]/ul/li[8]/a'))
    time.sleep(10)
    webdriver.switch_to.window(webdriver.window_handles[-1])
    copy=webdriver.find_element_by_xpath('//*[@id="litotxt"]/a')
    webdriver.execute_script('arguments[0].click()',copy)

    time.sleep(5)
    webdriver.close()
    webdriver.switch_to.window(webdriver.window_handles[0])#转到第一个窗口
    webdriver.find_element_by_xpath('//*[@id="gridTable"]/div[1]/div[2]/div[1]/a').click()#清除已选文献
    time.sleep(2)


for j in range(12):
    get_text()






'''更频繁面临的另一个问题是需要滚动到网页的底部。您可以在一行代码中执行此操作：

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

'''

