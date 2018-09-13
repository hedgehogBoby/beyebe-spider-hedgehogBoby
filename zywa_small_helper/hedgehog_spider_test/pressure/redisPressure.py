from zywa_database_core.dao.redis.redisTest import redisKeys, redisLlen, redisScard

if __name__ == '__main__':
    for i in range(2, 4):
        print('redis' + str(i))
        keys = redisKeys(i)
        for key in keys:
            try:
                num = redisLlen(i, key)
            except:
                pass
            try:
                num = redisScard(i, key)
            except:
                pass
            print('[KEY]:{} [NUM]:{}'.format(key.decode(), num))
