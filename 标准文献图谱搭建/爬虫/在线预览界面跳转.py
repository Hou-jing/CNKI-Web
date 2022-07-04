#在线预览界面
import time

import ddddocr
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

driver=webdriver.Chrome(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\102.0.5005.115\\chromedriver')
id='71F772D7F3B3D3A7E05397BE0A0AB82A'
detail_base_url='http://std.samr.gov.cn/gb/search/gbDetailed?id={}'.format(id)
driver.get(detail_base_url)

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
element=driver.find_element_by_xpath('//div[5]/div/div[1]')
ActionChains(driver).move_to_element(element).perform()
down_data_click = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[5]/div/div[1]"))
            )
time.sleep(2)
down_data_click.click()




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
#图片裁剪，不能直接request.get()因为，图片会刷新，验证码会识别失败，其次，必须在新界面打开，保证验证码不在刷新
cropped = Image.open("抓取1.png").crop((530, 380, 750, 500))  # (left, upper, right, lower)
cropped.save('code.png')
ocr = ddddocr.DdddOcr()
#验证码识别
res = ocr.classification(open('code.png', 'rb').read())
driver.switch_to.window(driver.window_handles[-2])
driver.find_element_by_xpath('//*[@id="verifyCode"]').send_keys(res)
driver.find_element_by_xpath('//*[@id="myModal"]/div/div/div[3]/button').click()
time.sleep(3)
