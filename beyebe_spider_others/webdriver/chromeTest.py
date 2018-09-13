
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/Users/magic/PycharmProjects/zywa-spider-xiaociwei/plug/chromedriver/mac/chromedriver')
driver.maximize_window()
driver.get('http://www.goudaitv.com/play/3522-0-0.html')
source = driver.page_source
bs4 = BeautifulSoup(source)
for iframeTag in bs4.select('iframe'):
    # http://api.goudaitv.com/Yunflv/zhilian.php?v=http://bf.ahpai.cc/20180715/c9D4UA7s/index.m3u8
    src = iframeTag['src']
    print(src)
    if 'http://api.goudaitv.com/Yunflv/zhilian.php?v=' in src:
        print("找到目标地址")
        url = src.replace('http://api.goudaitv.com/Yunflv/zhilian.php?v=', '')
        print(url)

print(driver)
