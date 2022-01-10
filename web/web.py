
import time
from selenium.webdriver.common.action_chains import ActionChains
import selenium
from selenium import webdriver
#import tesserocr#识别图片验证码
from  selenium.webdriver.common.keys import Keys

#20行转不到登录界面
webdriver=webdriver.Chrome('C:\\Program Files (x86)\\Google\\Update\\1.3.36.112\\chromedriver.exe')
webdriver.get('https://www.webofscience.com/wos/alldb/basic-search')
webdriver.find_element_by_xpath('//*[@id="mat-select-0"]/div/div[1]').click()
element=webdriver.find_element_by_xpath('//*[@id="mat-option-14"]/span')
ActionChains(webdriver).move_to_element(element).click().perform()
webdriver.find_element_by_xpath('/html/body/microui-app/div/section/microui-base/div[1]/div/base-login/div/div[3]/div[3]/app-shibboleth-login/div/form/button').click()
element=webdriver.find_element_by_xpath('//*[@id="app"]/section/section/main/div/div[2]/div[2]/div/div[1]/div/input')
ActionChains(webdriver).move_to_element(element).click().perform()

# element=webdriver.find_element_by_xpath('//*[@id="app"]/section/section/main/div/div[1]/div[2]/div/div')
# ActionChains(webdriver).move_to_element(element).click().perform()
time.sleep(2)
webdriver.find_element_by_xpath('//*[@id="app"]/section/section/main/div/div[2]/div[1]').click()#前往登录
time.sleep(10)
webdriver.find_element_by_xpath('/html/body/microui-app/div/section/div[2]/microui-base/div[1]/div/base-login/div/div[3]/div[3]/app-shibboleth-login/div/form/button/span').click()
webdriver.find_element_by_xpath('//*[@id="userName"]').send_keys('houjing21@mails.ucas.ac.cn')
webdriver.find_element_by_xpath('//*[@id="password"]').send_keys('v3CdDgpuCd')
webdriver.find_element_by_xpath('//*[@id="loginBtn"]').click()
time.sleep(5)
#账号密码登录
# webdriver.find_element_by_xpath('//*[@id="mat-input-0"]').send_keys('2960240482@qq.com')
# webdriver.find_element_by_xpath('//*[@id="mat-input-1"]').send_keys('hou@18833283973')
# webdriver.find_element_by_xpath('//*[@id="signIn-btn"]').click()
webdriver.find_element_by_xpath('//*[@id="snSelectDb"]/button/span[1]').click()
time.sleep(1)
webdriver.find_element_by_xpath('//*[@id="global-select"]/div/div[2]/div[2]/span').click()

webdriver.find_element_by_xpath('//*[@id="snSearchType"]/div[1]/app-search-row/div/div[2]/input').send_keys('complex network',Keys.ENTER)
webdriver.find_element_by_xpath('//*[@id="snSearchType"]/div[2]/button[2]/span[1]').click()
webdriver.find_element_by_xpath('//*[@id="global-select"]/div/div/div[1]').click()
webdriver.find_element_by_xpath('//*[@id="global-select"]/div[1]/div/div[4]/span').click()
webdriver.find_element_by_xpath('//*[@id="snSearchType"]/div[2]/app-search-timespan/div/div[2]/input[1]').send_keys('1995-01-01')
webdriver.find_element_by_xpath('//*[@id="snSearchType"]/div[2]/app-search-timespan/div/div[2]/input[2]').send_keys('2021-12-30')
webdriver.find_element_by_xpath('//*[@id="snSearchType"]/div[4]/button[2]/span[1]').click()
time.sleep(3)
webdriver.find_element_by_xpath('/html/body/app-wos/div/div/main/div/div[2]/app-input-route/app-base-summary-component/div/div[2]/app-page-controls[1]/div/app-sort-option/wos-select/button/span[2]').click()
webdriver.find_element_by_xpath('//*[@id="global-select"]/div/div[2]/div[1]').click()
time.sleep(2)
webdriver.find_element_by_xpath('//*[@id="mat-checkbox-158"]/label').click()
webdriver.find_element_by_xpath('/html/body/app-wos/div/div/main/div/div[2]/app-input-route/app-base-summary-component/div/div[2]/app-page-controls[1]/div/form/div/button[2]/span[1]/mat-icon').click()
time.sleep(2)





