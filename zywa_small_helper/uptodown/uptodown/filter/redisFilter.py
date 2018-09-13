import redis
from scrapy.dupefilter import BaseDupeFilter

from zywa_database_core.dao.redis.redisTest import poolList

"""
1. 根据配置文件找到 DUPEFILTER_CLASS = 'xianglong.dupe.MyDupeFilter'
2. 判断是否存在from_settings
    如果有：
        obj = MyDupeFilter.from_settings()
    否则：
        obj = MyDupeFilter()
"""


class CommonRedisFilter(BaseDupeFilter):
    r = redis.Redis(connection_pool=poolList[2])

    def __init__(self):
        self.record = set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    #:return: True表示已经访问过；False表示未访问过
    def request_seen(self, request):
        # TODO 自己实现一个基于redis的去重
        #:return: True表示已经访问过；False表示未访问过
        return False

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        pass
