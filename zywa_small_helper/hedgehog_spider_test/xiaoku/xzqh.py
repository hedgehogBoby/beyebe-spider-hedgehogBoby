# -*- coding:utf-8 -*-
'''
获取国家统计局上的行政区划码
'''
import requests, re

base_url = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201504/t20150415_712722.html'


def get_xzqh():
    html_data = requests.get(base_url).content
    pattern = re.compile('<p class="MsoNormal" style=".*?"><span lang="EN-US" style=".*?">(\d+)<span>.*?</span></span><span style=".*?">(.*?)</span></p>')
    areas = re.findall(pattern, html_data)
    print("code,name,level")

    for area in areas:
        print(area[0], area[1].decode('utf-8').replace(u'　', ''), area[1].decode('utf-8').count(u'　'))


if __name__ == '__main__':
    get_xzqh()
