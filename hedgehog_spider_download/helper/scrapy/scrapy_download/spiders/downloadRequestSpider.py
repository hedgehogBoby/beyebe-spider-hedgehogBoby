import traceback
from scrapy_redis.spiders import RedisSpider

from hedgehog_base_core.dao.mongo.mongoClientNew import saveToDownloadTable
from hedgehog_base_core.dao.redis.redisTest import redisLPush, redisErrorSend, redisMissionBeanMsgSave, redisConut
from hedgehog_spider_download.helper.scrapy.scrapy_download.util.decodeMyself import decodeMyself


class DownloadRequestSpider(RedisSpider):
    """
    使用scrapy-redis下发任务
    """
    name = "scrapy_download"
    redis_key = "hedgehog_scrapy:strat_urls"

    def parse(self, response):
        """
        需要将合理的对象入库,并且下发下一个任务
        :param response:
        :return:
        """
        try:
            print("成功进行Request解析:" + response.url)
            # 如果是301跳转，将跳转的页面重新放入redis队列以重新消费
            if response.status == 301:
                print("是301跳转，将跳转页置入redis末尾")
                url = response.headers['Location'].decode()
                print("跳转至:" + url)
                missionBean = response.request.missionBean
                missionBean.url = url
                key = '5_' + missionBean.downloadMethod
                redisLPush(3, key, missionBean.getRedisDict())
                return None

            # 入库
            html = decodeMyself(response)
            # print(html)

            missionBean = response.request.missionBean
            try:
                XIAOCIWEI_BASE = "<xiaociwei data=\"{}\" type=\"{}\">"
                strReplace = ""
                try:
                    strReplace += XIAOCIWEI_BASE.format(str(response.url), 'url')
                except:
                    pass
                try:
                    strReplace += XIAOCIWEI_BASE.format(str(response.headers), 'headers')
                except:
                    pass
                try:
                    strReplace += XIAOCIWEI_BASE.format(str(response.encoding), 'encoding')
                except:
                    pass
                try:
                    strReplace += XIAOCIWEI_BASE.format(str(response.status_code), 'status_code')
                except:
                    pass
                html = html.replace('</head>', strReplace + '</head>', 1)
                missionBean.html = html
            except:
                pass
            if missionBean.html is None:
                missionBean.html = html
            # 存储mongo
            saveToDownloadTable(missionBean)
            # 下发通知
            redisMissionBeanMsgSave(missionBean)
            redisConut(missionBean.type, 'success')
            # 取下一个任务进入队列
            return None
        except:
            errMsg = traceback.format_exc()
            print("parse ERROR:" + errMsg)
            missionBean = response.request.missionBean
            redisErrorSend(missionBean.type, errMsg)
