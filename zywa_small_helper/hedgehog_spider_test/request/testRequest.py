import json
import re

import requests
from bs4 import BeautifulSoup

url = 'https://s.search.bilibili110.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=183&page=1&pagesize=20&jsonp=jsonp&time_from=20180602&time_to=20180609&_=1528510256558'
url = 'http://news.163.com/rank/'
url = 'http://list.iqiyi.com/www/1/-------------11-7-1-iqiyi--.html'
url = 'http://www.iqiyi.com/v_19rrh4moi8.html'
# ip = getRandomOneIP()
# proxies = {"http": "http://198.15.135.26:8090", "https": "https://198.15.135.26:8090", }
html = requests.get(url).text
# soup = BeautifulSoup(html, "html.parser")
# print(soup.prettify())
msgStr = re.search(":page-info='(.*?)'", html).group(1)
msgStr2 = re.search(":video-info='(.*?)'", html).group(1)
jsonObj = json.loads(msgStr)
jsonObj2 = json.loads(msgStr2)
print(jsonObj2)
