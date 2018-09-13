import platform
import ssl

import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Proxy
from selenium.webdriver.common.proxy import ProxyType

from zywa_ippool_util.helper.iPPoolHelper import getRandomOneIP


def webDriverPhantomJS(url, **kwargs):
    ssl._create_default_https_context = ssl._create_unverified_context
    print("[info]webDriver:设置Header/代理IP")
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
    )
    ipDict = getRandomOneIP()
    proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': ipDict['ip'] + ':' + ipDict['port']})  # 代理ip和端口
    proxy.add_to_capabilities(dcap)
    print("[info]webDriver:获取代理IP成功{}".format(str(ipDict)))
    if 'Linux' in platform.system():
        driver = webdriver.PhantomJS(executable_path='/root/xiaociwei_download/zywa_crawl_platform/plug/geckodriver/phantomjs-2.1.1-linux-x86_64/bin/phantomjs', service_args=['--ssl-protocol=any'], desired_capabilities=dcap)
    else:
        driver = webdriver.PhantomJS(executable_path='/Users/magic/PycharmProjects/zywa-spider-xiaociwei/plug/geckodriver/phantomjs-2.1.1-macosx/bin/phantomjs', service_args=['--ssl-protocol=any'], desired_capabilities=dcap)
    try:
        print("[info]webDriver:初始化webDriver成功")
        driver.get(url)
        print("[info]webDriver:访问成功")
        __doAction(kwargs.get('action'), driver)
        print("[info]执行操作码成功")
        driver.save_screenshot('test2.png')
        return driver.page_source
    finally:
        print("[info]关闭driver成功")
        driver.quit()


def __doAction(actionList, driver):
    # action具有很大的不稳定性,但是是很重要的操作,请自行处理异常
    # 2018/5/31 为参数设定了一些默认值
    if actionList is None:
        print("无操作指令,返回")
        return
    for actionNow in actionList:
        tStart = int(time.time())
        # actionNow转对象
        print("正在执行操作:" + str(actionNow))
        if actionNow.get('name') == 'waitfor':
            print('[INFO]执行waitfor操作')
            while True:
                if int(time.time()) - tStart > actionNow.get('timeout', 10):
                    print('[WARNING]执行waitfor操作超时')
                    break
                if actionNow.get('msg', "") in driver.page_source:
                    break
            time.sleep(0.01)
        if actionNow.get('name') == 'delay':
            print('[INFO]执行delay操作')
            time.sleep(actionNow.get('timeout', 10))
        if actionNow.get('name') == 'pushdown':
            print('[INFO]执行pushdown操作')
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(actionNow.get('timeout', 1))
        if actionNow.get('name') == 'js':
            print('[INFO]执行js操作')
            driver.execute_script(actionNow.get('msg', ''))
            time.sleep(actionNow.get('timeout', 1))


if __name__ == '__main__':
    print(webDriverPhantomJS('https://www.baidu.com', action=[{'name': 'delay'}]))
