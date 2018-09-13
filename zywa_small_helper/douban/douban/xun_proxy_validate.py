import requests
import pymongo
import json
import time
import traceback
import threading
import redis
import json
import datetime
import logging
import sys

# client = pymongo.MongoClient("mongodb://172.10.3.157:27017/")
# db = client.proxy
# col_log = db.xun_proxy

# 日志配置
logger = logging.getLogger()
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

REDIS_CONNECT_INFO_COMMON = {
    "host": "172.10.3.157",
    "port": 16379,
    "password": "",
    "db": 3,
}

r_commen = redis.Redis(host=REDIS_CONNECT_INFO_COMMON['host'], port=REDIS_CONNECT_INFO_COMMON['port'],
                       db=REDIS_CONNECT_INFO_COMMON['db'], password=REDIS_CONNECT_INFO_COMMON['password'])


def validate():
    try:
        base_url = 'https://www.baidu.com/'
        ip = r_commen.rpop('ippool_2')
        if ip:
            ip_json = ip.decode()
            ip_dict = json.loads(ip_json)
            ips = 'https://' + ip_dict['ip'] + ':' + ip_dict['port']
            ip = 'http://' + ip_dict['ip'] + ':' + ip_dict['port']
            proxies = {'https': ips, 'http': ip}
            validate = requests.get(base_url, proxies=proxies, verify=False, timeout=2)
            if validate.status_code == 200:
                r_commen.lpush('ippool_2', ip_json)
                logger.info(str(datetime.datetime.now()) + '--------------------该代理有效------------------------')
            else:
                logger.info(str(datetime.datetime.now()) + '********************已删除无效代理*********************')
        else:
            logger.info(str(datetime.datetime.now()) + "***************************IP池为空**************************")
    except:
        logger.info(traceback.format_exc())


if __name__ == '__main__':
    while True:
        for i in range(5):
            t = threading.Thread(target=validate, )
            t.start()
            time.sleep(0.5)
        # validate()
        # time.sleep(0.5)

        # ip_sql =  col_log.find({})
    # for i in ip_sql:
    #     ips = 'https://' +  i['ip'] + ':' + i['port']
    #     ip = 'http://' +  i['ip'] + ':' + i['port']
    #     proxies = {'https': ips ,'http' : ip}
    #     # requests.get("http://example.org", proxies=proxies)
    #     try:
    #         validate = requests.get(base_url,proxies=proxies,verify=False,timeout=2)
    #         if validate.status_code == 200:
    #             print('--------------------该代理有效------------------------')
    #         else:
    #             col_log.delete_one({'ip':i['ip']})
    #             print('------------------已删除无效代理----------------------')
    #     except:
    #         col_log.delete_one({'ip':i['ip']})
    #         print('------------------已删除无效代理----------------------')
