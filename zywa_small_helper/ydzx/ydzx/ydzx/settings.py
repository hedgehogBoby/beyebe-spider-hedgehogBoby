# -*- coding: utf-8 -*-

BOT_NAME = 'ydzx'

SPIDER_MODULES = ['ydzx.spiders']
NEWSPIDER_MODULE = 'ydzx.spiders'
ROBOTSTXT_OBEY = False
SPIDER_MIDDLEWARES = {
    'scrapy.dupefilter.RFPDupeFilter': None,
}
COOKIE = 'sptoken=Uhoy~U9%3AU%3E%3AU48261efeced332cc9f20413132c69381b10fa38be1a919434984fe954c995cb0; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1529565465; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1529562826,1529563716,1529564193,1529565428; UM_distinctid=15a895560d9fe-09db3b167f4fe78-6b2e254a-1aeaa0-15a895560da974; cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%2215a895560d9fe-09db3b167f4fe78-6b2e254a-1aeaa0-15a895560da974%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201529565450%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201529565450%7D%7D; CNZZDATA1255169715=1069830291-1529561488-null%7C1529561488; captcha=s%3A9ea6f22c17d78391f4beba2f0b2b9f93.e6WR5CIrgZI3unvoZb%2FJlcWAVxp9uJTLh7EWI4aFsw4; JSESSIONID=a05b645336b1a05fb5086fa8b66c92252556a46e05e7b38cda8e786a25e06701; weather_auth=2; cn_9a154edda337ag57c050_dplus=%7B%22distinct_id%22%3A%20%2215a895560d9fe-09db3b167f4fe78-6b2e254a-1aeaa0-15a895560da974%22%2C%22%E6%9D%A5%E6%BA%90%E6%B8%A0%E9%81%93%22%3A%20%22%22%2C%22initial_view_time%22%3A%20%221488366578%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201509853314%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201509853314%7D%7D; wuid=539818983577421; wuid_createAt=2017-05-07 16:24:25'
