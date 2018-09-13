# -*- coding: utf-8 -*-
import requests
import random, re
from bs4 import BeautifulSoup
from xpinyin import Pinyin

"""
2018/08/17 by xiaociwei

基于抓取行政区划城市名，完成城市接龙。
如果城市名过少,可在getCityList中 TODO 处增加抓取深度，默认为2
<--个人信息-->
姓名 方楠
电话 16607557430
可直接电话联系。
"""

URL_BASE = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/'
cityMap = {}  # 存储城市名
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
]
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
p = Pinyin()


# city更新
def __cityUpdate(aTags):
    for aTag in aTags:
        aTitle = aTag.text
        if len(aTitle) > 0:
            if aTitle == '市辖区' or '京ICP' in aTitle or not __contain_zh(aTitle):
                continue
            key = p.get_pinyin(aTitle[0])
            if key in cityMap:
                cityMap[key].append(aTitle)  # 加入城市列表
            else:
                cityMap.update({key: [aTitle]})  # 加入城市列表


# 汉字识别工具
def __contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    global zh_pattern
    match = zh_pattern.search(word)

    return match


# http请求封装
def __httpGet(url):
    headers = {
        'User-Agent': random.choice(user_agent),
        'Content-Type': 'charset=gb2312'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    # response.encoding = 'gb2312'

    return response.text


# 广度递归抓取封装
def __deepExtract(aTags):
    aTagsNew = []
    for aTag in aTags:
        aUrl = URL_BASE + aTag['href']
        aTitle = aTag.text
        if aTitle == '市辖区' or '京ICP' in aTitle or not __contain_zh(aTitle):
            continue
        print('正在抓取', aTitle)
        html = __httpGet(aUrl)
        aTags = BeautifulSoup(html, "html.parser").select('a')
        aTagsNew.extend(aTags)
        __cityUpdate(aTags)
    return aTagsNew


# 通过行政区划抓取,抓取城市列表
def getCityList():
    url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html'
    # 根据反爬需求，这里可以定制headers\代理ip\ua等。
    # 个人习惯用scrapy开发，鉴于依赖包比较重就用requests简单开发。

    aTags = BeautifulSoup(__httpGet(url), "html.parser").select('a')
    __cityUpdate(aTags)
    # TODO 2层广度优先，如果您时间充裕，可以多抓几层。
    for deep in range(1):
        print('正在抓取第', deep + 1, '层')
        aTags = __deepExtract(aTags)


if __name__ == '__main__':
    print("正在抓取地名,请稍后...")
    getCityList()
    print(cityMap)
    city = input('输入城市名字：\n')
    # 根据尾部拼音索引Map,从对应list中随机获取一个地名
    print('结尾拼音是', p.get_pinyin(city[-1]))
    print(random.choice(cityMap.get(p.get_pinyin(city[-1]), [])))
