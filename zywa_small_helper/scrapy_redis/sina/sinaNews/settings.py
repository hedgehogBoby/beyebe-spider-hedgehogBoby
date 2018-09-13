SPIDER_MODULES = ['sinaNews.spiders']
NEWSPIDER_MODULE = 'sinaNews.spiders'

# 使用scrapy-redis里的去重组件，不使用scrapy默认的去重方式
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy-redis里的调度器组件，不使用默认的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True
# 默认的scrapy-redis请求队列形式（按优先级）
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 队列形式，请求先进先出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 栈形式，请求先进后出
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

# 只是将数据放到redis数据库，不需要写pipelines文件
ITEM_PIPELINES = {
    #    'Sina.pipelines.SinaPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1
# 指定redis数据库的连接参数
REDIS_HOST = '192.168.10.9'
REDIS_PORT = 6379

# 指定 redis链接密码，和使用哪一个数据库
REDIS_PARAMS = {
    'password': '123456',
    'db': 1
}

# REDIS_URL = 'redis://:123456@192.168.10.9:6379/2'
