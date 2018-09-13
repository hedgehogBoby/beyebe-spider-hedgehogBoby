import hashlib

import requests
import time

url = 'http://dyt1.oss-cn-shenzhen.aliyuncs.com/dianyou/data/circle/img/20180723/410c05de-8e24-11e8-8e99-acde48001122.mp4'
file = requests.get(url, timeout=30).content
print("下载完毕,正在获取md5")
start = int(time.time())

print(int(time.time()) - start)


def getMd5(file):
    m0 = hashlib.md5()
    m0.update(file)
    return m0.hexdigest()
