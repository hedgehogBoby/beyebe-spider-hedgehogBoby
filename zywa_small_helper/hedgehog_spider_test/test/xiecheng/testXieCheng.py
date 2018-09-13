from random import random
from time import sleep

import gevent
from gevent.pool import Group


def intensive(n):
    gevent.sleep(n['delay'])
    n['text'] = 'ok download Success!'
    return n


igroup = Group()


def requestTest():
    # 请求来啦
    i = igroup.imap_unordered(intensive, [{'delay': random()}])
    print("成功完成模拟下载任务,结果" + i[0])


if __name__ == '__main__':
    requestTest()
