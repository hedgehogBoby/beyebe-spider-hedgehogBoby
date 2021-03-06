import grequests
import time
import requests

urls = [
    'https://docs.python.org/2.7/library/index.html',
    'https://docs.python.org/2.7/library/dl.html',
    'http://www.iciba.com/partial',
    'http://2489843.blog.51cto.com/2479843/1407808',
    'http://blog.csdn.net/woshiaotian/article/details/61027814',
    'https://docs.python.org/2.7/library/unix.html',
    'http://2489843.blog.51cto.com/2479843/1386820',
    'http://www.bazhuayu.com/tutorial/extract_loop_url.aspx?t=0',
]


def method1():
    t1 = time.time()
    for url in urls:
        res = requests.get(url)
        # print res.status_code

    t2 = time.time()
    print('method1', t2 - t1)


def method2():
    rs = (grequests.get(u) for u in urls)
    t1 = time.time()
    res = grequests.map(rs, size=3)
    #    print res
    t2 = time.time()
    print('method2', t2 - t1)


def method3():
    rs = (grequests.get(u) for u in urls)
    t1 = time.time()
    res = grequests.map(rs, size=6)
    #    print res
    t2 = time.time()
    print('method3', t2 - t1)


if __name__ == '__main__':
    method1()
    method2()
    method3()
