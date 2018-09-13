import configparser
import datetime
import json
import traceback
import uuid

import os
import redis

# r2 = redis.Redis(host="172.10.3.157", port=16379, db=2)

current_path = os.path.dirname(__file__)
current_path = current_path[:current_path.find('beyebe-spider-xiaociwei')+len('beyebe-spider-xiaociwei')]
cf = configparser.ConfigParser()
cf.read(current_path+"/configMyself.conf", "utf-8")

REDIS_IP = cf.get("redis", "ip")
REDIS_PORT = cf.get("redis", "port")
REDIS_PASSWORD = cf.get("redis", "password")

poolList = []
for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
    poolList.append(redis.ConnectionPool(host=REDIS_IP, password=REDIS_PASSWORD, port=int(REDIS_PORT), db=i))


def redisKeys(poolId):
    r = redis.Redis(connection_pool=poolList[poolId])
    return r.keys()


def redisSaveAll3(key, lstItem):
    for i in lstItem:
        redisDownloadSaveDb3(key, i)


# 使用业务
# 1、个性化私有IP池存储
# 2、监控框架记录
def redisSet(poolId, key, item):
    try:
        item = json.dumps(item)
        r = redis.Redis(connection_pool=poolList[poolId])
        r.set(key, item)
        print('redis set 成功')
    except:
        print('[ERROR]redis3 Save Error!')
        traceback.print_exc()


def redisGet(poolId, key):
    try:
        r = redis.Redis(connection_pool=poolList[poolId])
        strNow = r.get(key)
        if strNow is None:
            # print('不存在该key[redis-get]')
            return None
        print('redis get 成功')
        return strNow.decode()
    except:
        print('[ERROR]redis3 get Error!')
        traceback.print_exc()


def redisLPush(poolId, key, item):
    try:
        if type(item) == type({}):
            item = json.dumps(item, ensure_ascii=False)
        r = redis.Redis(connection_pool=poolList[poolId])
        return r.lpush(key, item)
    except:
        print('[ERROR]redis lpush Error!')
        traceback.print_exc()


def redisSelectAll3(key):
    r = redis.Redis(connection_pool=poolList[3])
    bList = r.lrange(key, 0, -1)
    strList = []
    for i in bList:
        strList.append(i.decode())
    print('redis 查询成功,查询数:' + str(len(strList)))
    return strList


def redisSadd(poolId, key, value):
    try:
        r = redis.Redis(connection_pool=poolList[poolId])
        # print('[info]redis3 spop')
        if r.sadd(key, value) == 1:
            return True
        else:
            return False
    except Exception as err:
        print('[ERROR]redis3 spop Error!' + str(err))
        return False


# 使用业务：
# 1、业务机_下载队列回调 pool3
# 2、IP池获取 pool3
# 3、解析机_通知队列回调 pool4
def redisRPop(i, key, **kwargs):
    r = redis.Redis(connection_pool=poolList[i])
    bStr = r.rpop(key)
    # print('redis pop操作成功')
    if bStr is None:
        if kwargs.get('log', False):
            print(key + '_无数据,返回None')
        return None
    return bStr.decode()


# 设置key过期时间，使用业务:
# 1、监控框架
def redisExpire(poolId, key, second):
    r = redis.Redis(connection_pool=poolList[poolId])
    return r.expire(key, second)


def redisScard(poolId, key):
    """
    获取集合的个数
    """
    r = redis.Redis(connection_pool=poolList[poolId])
    num = r.scard(key)
    # print('redis pop操作成功')
    return num


# 使用业务:
# 1、测试redis接口
def redisLlen(poolId, key):
    """
    获取队列的长度
    """
    r = redis.Redis(connection_pool=poolList[poolId])
    num = r.llen(key)
    # print('redis pop操作成功')
    return num


def redisIncr(poolId, key):
    try:
        r = redis.Redis(connection_pool=poolList[poolId])
        r.incr(key)
        print('redis incr 成功')
    except:
        print('[ERROR]redis3 incr Error!')
        traceback.print_exc()


# redis去重
def redisRepeat(key, repeatId):
    try:
        key = 'channel_' + str(key)
        repeatId = str(repeatId)
        return redisSadd(2, key, repeatId)
    except:
        print('[ERROR]redis3 Save Error!')
        traceback.print_exc()


# 从set中随机返回一个元素
def redisSpop(poolId, key):
    try:
        r = redis.Redis(connection_pool=poolList[poolId])
        print('[info]redis3 spop')
        return r.spop(key).decode()
    except:
        print('[ERROR]redis3 spop Error!')
        traceback.print_exc()


"""
具体业务使用
"""


# 分发机推送下载
def redisDownloadSaveDb3(key, item):
    try:
        if '_id' in item:
            item['_id'] = str(item['_id'])
        if type({}) == type(item):
            item = json.dumps(item, cls=DateEncoder)
        r = redis.Redis(connection_pool=poolList[3])
        isLog = False
        while True:
            if r.llen(key) < 10000:
                r.lpush(key, item)
                break
            if not isLog:
                print("下载队列已满,请降低下载压力")
                isLog = True

        pass
    except:
        print('[ERROR]redis3 Save Error!')
        traceback.print_exc()


# 分发机获取下载机回调
def redisCallBackSaveDb3(redisKey, missionBean):
    """
    download_callback
    """
    key = redisKey + '_callback_' + str(missionBean.type)
    item = missionBean.getRedisDict()
    try:

        if type({}) == type(item):
            item = json.dumps(item)
        r = redis.Redis(connection_pool=poolList[3])
        r.lpush(key, item)
        print('callback_redis3保存成功')
        pass
    except:
        print('[ERROR]redis3 Save Error!')
        traceback.print_exc()


# 分发机获取下载机回调Set
def redisCallBackSaveDb3Set(redisKey, missionBean):
    """
    download_callback
    """
    key = redisKey + '_callback_' + str(missionBean.type)
    key = key + ':' + missionBean.url
    item = missionBean.getRedisDict()
    try:

        if type({}) == type(item):
            item = json.dumps(item)
        r = redis.Redis(connection_pool=poolList[3])
        r.set(key, item)
        # 一周过期时间
        r.expire(key, 60 * 60 * 24 * 7)
        print('callback_redis3 set 保存成功')
        pass
    except:
        print('[ERROR]redis3 Save Error!')
        traceback.print_exc()


# 下发通知
def redisMissionBeanMsgSave(missionBean):
    """
    下载完的missionBean通知队列,只保存docId type url downloadId
    :return:
    """
    item = {}
    item['url'] = missionBean.url
    item['downloadId'] = missionBean.downloadId
    item['docId'] = missionBean.__dict__.get('docId', '0')
    item['type'] = missionBean.type
    return redisLPush(3, missionBean.downloadMethod + '_callback_' + str(missionBean.type), json.dumps(item))


# 获取最高优先级Key
def redisGetBiggetDeepKey(poolId, aimKey, **kwargs):
    """
    查询所有Key,找到符合num_aimKey结构中,num最大的key
    :param poolId:
    :param aimKey:
    :return:
    """

    r = redis.Redis(connection_pool=poolList[poolId])
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    bKeys = r.keys()
    # 首先判断是否有优先级的存在
    for i in range(9, kwargs.get('minLevel', -1), -1):
        for keyNow in bKeys:
            keyNow = keyNow.decode()
            strTest = str(i) + '_' + aimKey
            if strTest == keyNow:
                return strTest
            strTest = str(i) + '_' + aimKey + '_' + mac
            if strTest == keyNow:
                return strTest
    # 再直接删除优先级逻辑直接查询
    for i in range(9, -1, -1):
        for keyNow in bKeys:
            keyNow = keyNow.decode()
            strTest = str(i) + '_' + aimKey
            if strTest == keyNow:
                return strTest
            strTest = str(i) + '_' + aimKey + '_' + mac
            if strTest == keyNow:
                return strTest
    # 随后判断本身是否存在
    for keyNow in bKeys:
        keyNow = keyNow.decode()
        strTest = aimKey
        if strTest == keyNow:
            return strTest
    return None


# 获取所有IP
def redisLRangeToDict(poolId, key):
    r = redis.Redis(connection_pool=redis.ConnectionPool(host="172.10.3.157", port=16379, db=3))
    list = r.lrange(key, 0, -1)
    dictList = []
    for i in list:
        dictList.append(json.loads(i.decode()))
    return dictList


# 计数日志
def redisConut(typeNum, kindStr):
    nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在
    key = 'count_' + str(typeNum) + ':' + nowTime + ':' + kindStr
    if typeNum >= 10000:
        key = 'test:' + key
    redisIncr(15, key)
    key = 'count_total:' + nowTime + ':' + kindStr
    if typeNum >= 10000:
        key = 'test:' + key
    redisIncr(15, key)


# 错误日志
def redisErrorSend(typeNum, errorMsg):
    nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在
    key = 'count_' + str(typeNum) + ':' + nowTime + ':error'
    if typeNum >= 10000:
        key = 'test:' + key
    redisLPush(15, key, errorMsg)


# 解析时回调使用
def redisParseSend(missionBean, keyList):
    """
    使用时，把你需要传递的信息放入missionBean中，并标明需要传递的字段List
    其中最小存储单元url type docId downloadId不必再声明
    举例:
        missionBean.msg='test'
        redisParseSend(missionBean,['msg']):
    结果：
        将四个最小存储单元加上msg存入回调队列
    :param missionBean:
    :return:
    """
    key = 'parse_callback_' + str(missionBean.type)
    dictNow = missionBean.getEasyDict()
    for minKey in keyList:
        dictNow[minKey] = missionBean.__dict__.get(minKey)
    redisLPush(4, key, dictNow)


if __name__ == '__main__':
    r = redis.Redis(connection_pool=poolList[14])
    r.lpush('test_key', 'test')
    print(r.keys())
    # redisConut(10086, 'total')
    # redisErrorSend(10086, 'testError')
    redisLPush(3, 'webdriver_callback_11', 'test')
    # redisSpop(4, 'postgreSql_search_name')

    print(redisLlen(3, '6_request_common_file'))
    print(redisLlen(4, 'data_clear_1001'))
    # for i in range(1000000):
    #     redisRPop(4, 'data_clear_1001')
    #     print(1)
