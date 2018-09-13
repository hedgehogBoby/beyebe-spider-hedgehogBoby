import time


def log(*args, **kwargs):
    dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open('cang_log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


"""
掏粪工具箱

urlparse 直接解析出网址的路径
from urllib.parse import urlparse

url = "http://172.10.3.123/group3/M00/94/5D/rAoDIFsPwemAFIrbACr8pnV94k02995111"
parse = urlparse(url)
print(parse, type(parse))
print(parse.path)
https://my.oschina.net/u/2474096/blog/1593377
"""
