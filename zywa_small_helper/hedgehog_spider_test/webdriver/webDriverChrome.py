import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print(1)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
print(2)
chrome_options.binary_location = '/opt/google/chrome/chrome'
if 'Linux' in platform.system():
    opener = webdriver.Chrome(executable_path='/root/xiaociwei_download/zywa_crawl_platform/plug/chromedriver/linux/chromedriver', chrome_options=chrome_options)
else:
    opener = webdriver.Chrome(executable_path='/Users/magic/PycharmProjects/zywa-spider-xiaociwei/plug/chromedriver/mac/chromedriver', chrome_options=chrome_options)
print(3)
opener.get('https://www.baidu.com')
print(4)
opener.save_screenshot('test3.png')
print(opener.page_source)
