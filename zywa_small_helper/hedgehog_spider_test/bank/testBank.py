# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from zywa_database_core.dao.mysql.mysqlClient import MysqlClient
from zywa_database_core.model.xiaociweiModel import BankName
from zywa_download_httpserver.impl.request.webdriverImpl import WebdriverImpl

connectUrl = 'mysql+pymysql://root:mypass@172.10.3.104:3306/xiaociwei?charset=utf8'
client = MysqlClient(connectUrl)

if __name__ == '__main__':
    driver = WebdriverImpl()
    html = driver.getText('http://www.cbrc.gov.cn/chinese/jrjg/index.html')
    soup = BeautifulSoup(html, 'html.parser')

    soup.prettify()
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    for divBig in soup.select('div[class=\"wai\"]'):
        classfiy = divBig.select('div[class=\"zi\"]')[0].get_text().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        for bank in divBig.select('li'):
            # 寻找第一个a标签
            aTag = bank.select('a')
            if len(aTag) > 0:
                url = aTag[0]['href']
                name = str(aTag[0].get_text()).replace('\r', '').replace('\n', '').replace('\t', '')
            else:
                url = ''
                name = str(bank.get_text()).replace('\r', '').replace('\n', '').replace('\t', '')
            dictNow = {'name': name, 'classfiy': classfiy, 'url': url}
            print(dictNow)
            bankName = BankName()
            bankName.name = dictNow.get('name')
            bankName.classify = classfiy
            bankName.url = dictNow.get('url')
            try:
                client.insert(bankName)
            except:
                pass
