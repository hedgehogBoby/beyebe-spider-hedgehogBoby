import time
from selenium.webdriver.chrome.webdriver import WebDriver

driver = WebDriver(executable_path="/Users/magic/PycharmProjects/zywa-spider-xiaociwei/plug/chromedriver/mac/chromedriver")
driver.get("http://202.110.217.69:7001/hsp/logonDialog_113.jsp")
driver.find_element_by_id("yhmInput").send_keys("371083198706245037")
time.sleep(0.5)
driver.find_element_by_id("mmInput").send_keys("2078")
time.sleep(0.5)
print('等待用户输入验证码')
yymCode=input()
driver.find_element_by_id("validatecodevalue1").send_keys(yymCode)

driver.find_element_by_class_name("logonBtn").click()
time.sleep(5)
# C1001
driver.find_element_by_id("C1001").click()
