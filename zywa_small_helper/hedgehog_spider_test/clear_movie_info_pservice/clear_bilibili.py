import random
import time

import redis
import requests

import config
from cang_utils import CangMongoClient, log


class ClearBiliBili:
    def __init__(self):
        client = CangMongoClient(
            db=config.mongo_db,
            user=config.mongo_user,
            password=config.mongo_password,
        )
        self.db = client.new_db

        pool = redis.ConnectionPool(
            host=config.redis_host, port=config.redis_port,
            password=config.redis_password, db=config.redis_db)
        self.r = redis.Redis(connection_pool=pool)

    def clear(self):
        """
        1. 从 hand_movie_name 读取所有数据
        2. 查询，对每一个数据全量查询  v_bilibili_movie_info 的 title 查看是否命中
        :return:
        db.v_bilibili_movie_info.find({'info.title':{$regex: /后来的我们/}})
        """
        for i, h in enumerate(self.db["hand_movie_name"].find()):
            title = h.get("movieName")
            log("正在处理 hand_movie_name 第{}个".format(i), title)
            if len(title) < 3:
                log("标题长度小于两个字符", title)
                continue

            self.query_one_movie(h)

    def query_one_movie(self, movie_info):
        title = movie_info.get("movieName")
        # 查询 v_bilibili_movie_info
        query = {
            'info.title': {
                "$regex": "{}".format(title)
            }
        }
        del movie_info["_id"]
        for j, info in enumerate(self.db['v_bilibili_movie_info'].find(query)):
            log("query_one_movie title匹配 正在处理第 {} 个".format(j))
            info_title = info.get("info").get("title")
            query2 = {
                "info.title": info_title
            }
            # redis mongo 联合去重
            if self.de_weight(
                    r=self.r, rule=info_title, redis_name=config.redis_dub_name,
                    mongodb=self.db, tablename="v_bilibili_movie_info_pservice_test", query=query2):
                self.redis_set_one(self.r, info_title)

                # 根据描述 和 tag 打分
                rate, tags = self.rating(title, info)
                log("电影{}的评分为{}".format(info_title, rate))
                # 保存临时表
                del info["_id"]
                info["info"]["relation"] = movie_info
                info["info"]["relation"]['rate'] = rate
                info["info"]["random"] = random.random()
                info["info"]["tags"] = tags
                info["info"]['rate'] = rate
                log("正在准备存入", info)
                self.db["v_bilibili_movie_info_pservice_test"].insert(info)

    def rating(self, title, info):
        """
        根据描述 和 tag 打分
        :param title: 电影名
        :param info: 电影信息
        :return:
        """
        rate = 0
        description = info.get("info").get("desc")
        av = info.get("info").get("aid")
        # 描述含有电影名 +1分
        if title in description:
            rate += 1
        # 请求电影信息 tag 包含电影名 +1 分
        url = "https://api.bilibili.com/x/tag/archive/tags?aid={}&jsonp=jsonp&_={}".format(av, int(time.time() * 1000))
        tags = self.request_tag(url)
        if title in tags:
            rate += 1
        return rate, tags

    @staticmethod
    def request_tag(url):
        r = requests.get(url)
        print("正在请求tag", r)
        if r.status_code == 200:
            data = r.json()
            tags = [d.get("tag_name") for d in data.get("data")]
            return tags
        else:
            # todo 代理
            log("请求")
            return []

    @staticmethod
    def de_weight(r, rule, redis_name, mongodb, tablename, query):
        """
        去重， 不重复返回 true, 重复返回false
        redis 去重 + mongo 去重
        :param query: mongo 数据库查询条件
        :param tablename: 查询数据库的表名
        :param mongodb: 数据库连接
        :param redis_name: redis去重名称
        :param r: redis 连接
        :param rule: 去重规则的字段
        :return: 不重复返回 true, 重复返回false
        """
        # print(not r.sismember(redis_name, rule))
        # print(mongodb[tab
        # lename].find_one(query) is None)
        return (not r.sismember(redis_name, rule)) and (mongodb[tablename].find_one(query) is None)

    @staticmethod
    def redis_set_one(r, news_id):
        """
        :param r: redis name
        :param news_id:
        """
        try:
            r.sadd(config.redis_dub_name, news_id)
        except Exception as e:
            log("存入 redis 失败", e)

    @staticmethod
    def get_proxy(r, name):
        pass


if __name__ == '__main__':
    c = ClearBiliBili()
    c.clear()
