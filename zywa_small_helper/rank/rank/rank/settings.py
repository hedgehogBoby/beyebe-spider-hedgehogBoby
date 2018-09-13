# -*- coding: utf-8 -*-

BOT_NAME = 'rank'

SPIDER_MODULES = ['rank.spiders']
NEWSPIDER_MODULE = 'rank.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

RETRY_ENABLED = False
# RETRY_TIMES = 99999

SPIDER_MIDDLEWARES = {
    'scrapy.dupefilter.RFPDupeFilter': None,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,

    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 100,
    'rank.middlewares.DownloadError': 102
}
