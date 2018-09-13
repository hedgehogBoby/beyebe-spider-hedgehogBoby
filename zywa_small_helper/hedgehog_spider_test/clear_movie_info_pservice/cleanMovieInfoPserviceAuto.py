import random
import time
import traceback

import requests
import sys

sys.path.append("/root/xiaociwei_download/zywa_crawl_platform")

from zywa_database_core.dao.mongo.mongoClientNew import db_spider
from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself

__mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")


def rating(title, info):
    """
    根据描述 和 tag 打分
    :param title: 电影名
    :param info: 电影信息
    :return:
    """
    rate = 0
    description = info.get("info").get("description")
    av = info.get("info").get("id")
    # 描述含有电影名 +1分
    if title in description:
        rate += 1
    # 请求电影信息 tag 包含电影名 +1 分
    url = "https://api.bilibili.com/x/tag/archive/tags?aid={}&jsonp=jsonp&_={}".format(av, int(time.time() * 1000))
    tags = request_tag(url)
    if title in tags:
        rate += 1
    return rate, tags


def request_tag(url):
    r = requests.get(url)
    print("正在请求tag", r)
    if r.status_code == 200:
        data = r.json()
        tags = [d.get("tag_name") for d in data.get("data")]
        return tags
    else:
        # todo 代理
        return []


def addTags():
    items = __mongoClient.find({'info.rate': {'$exists': False}}, tableName='v_bilibili_movie_pservice')
    for item in items:
        # 补充tags\打分
        info = item['info']
        try:
            movieName = info['relation']['movieName']
        except:
            movieName = info['passage']
            item['info']['relation'] = {}
            item['info']['relation']['movieName'] = movieName
        # aid = info['id']
        rate, tags = rating(movieName, item)
        item['info']['tags'] = tags
        item['info']['rate'] = rate
        item["info"]["relation"]['rate'] = rate
        # 补充relation
        itemHand = __mongoClient.find_one({'movieName': movieName}, tableName='hand_movie_name')
        itemHand.pop('_id')
        item["info"]["relation"].update(itemHand)
        # 补充随机数
        item["info"]["random"] = random.random()
        print('完成结构清洗', info['title'])
        if rate < 2:
            __mongoClient.update(item, tableName='v_bilibili_movie_pservice')
        else:
            item['etc'] = 2
            __mongoClient.update(item, tableName='v_bilibili_movie_pservice')
            try:
                __mongoClient.saveDict(item, tableName='v_bilibili_movie_pservice_cheak')
            except:
                # traceback.print_exc()
                print('已存在')


def filterAuto():
    items = __mongoClient.getClient(tableName='v_bilibili_movie_pservice').find(
        {'$and': [{'info.rate': 2}, {'$or': [{'etc': None}, {'etc': 'Null'}, {'etc': ''}]}]})
    for item in items:
        # print(item['info']['title'])
        try:
            aid = str(item['info']['aid'])
        except:
            aid = str(item['info']['id'])
            item['info']['aid'] = aid
        item.etc = 1
        db_spider['v_bilibili_movie_pservice'].save(item)
        db_spider['v_bilibili_movie_pservice_cheak'].save(item)


if __name__ == '__main__':
    while True:
        try:
            # 删除其他标签的结果
            print(__mongoClient.getClient(tableName='v_bilibili_movie_pservice').remove(
                {'$and': [{'info.typeid': {'$exists': True}}, {'info.typeid': {'$ne': '181'}}, {'info.typeid': {'$ne': '182'}}, {'info.typeid': {'$ne': '183'}}, {'info.typeid': {'$ne': '184'}}]}))
            # 增加缺失Tag
            addTags()
            # 将2级打分的结果直接完成过滤
            filterAuto()
        except:
            traceback.print_exc()
        finally:
            time.sleep(1)
