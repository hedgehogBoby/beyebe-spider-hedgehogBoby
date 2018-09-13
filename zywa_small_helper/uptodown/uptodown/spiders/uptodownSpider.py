# -*- coding: utf-8 -*-
import hashlib
import logging
import traceback
import uuid
from datetime import datetime

import redis
import scrapy
from pandas import json
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from pyquery import PyQuery as pq

from zywa_database_core.dao.postgre.relational_database_helper import TableHelper
from zywa_database_core.dao.redis.redisTest import poolList
from zywa_small_helper.uptodown.uptodown.items import UptodownItem


def md5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()


def redis_set_add(pool_id, key, item):
    try:
        if type(item) == type({}):
            item = json.dumps(item)
        r = redis.Redis(connection_pool=poolList[pool_id])
        return r.sadd(key, item)
    except Exception as e:
        print('[ERROR]redis lpush Error!', e)
        traceback.print_exc()


class UptodownspiderSpider(scrapy.Spider):
    name = 'uptodownSpider'
    start_urls = ['https://www.uptodown.com/android', "https://en.uptodown.com/android", ]
    rules = (
        # TODO： 这个深度抓取没写对
        # TODO：allow匹配 https://marvel-comics.uptodown.com/android
        Rule(LinkExtractor(allow=(r"/uptodown.com/android/", r"/android/search/")), follow=True),
    )
    r = redis.Redis(connection_pool=poolList[4])

    connect_info = {
        'dbtype': "postgres",
        'username': "postgres",
        'password': "123456",
        'host': '172.10.3.170',
        "port": '5432',
        'database': 'test_db',
    }
    table_name = "t_app_info_overseas"
    app_info = TableHelper(connect_info, table_name)
    download_info = TableHelper(connect_info, "t_apk_download_info_overseas")
    print("连接数据库postgres成功")

    r7 = redis.Redis(connection_pool=poolList[7])

    def parseDownload(self, response):
        # TODO 透传item信息需要request对象的帮助
        # TODO 重写filter方法来进行去重 DUPEFILTER_CLASS
        # TODO 循环抓取 通过赋值一个低优先级的request任务实现
        # TODO allowed_domains主域名过滤
        # TODO 文件系统宝静
        # TODO linux系统要特殊配置才能上线scrapy

        # 断点查看透传效果
        item = response.request.item
        url = response.url
        print("包含下载地址的url为", url)
        html = response.text
        # 调用解析，拿到结果，存库， 发建哥的redis， 存建哥的库
        # 解析之后的结果
        item["detail_html"] = html
        item["android_download_url"] = url

        result = self.__parseDownload(html, url)
        for field in item.fields:
            if field in result.keys():
                item[field] = result[field]
        print("item", item)
        # 现在已经拿到下载地址了，需要下载入文件系统，需要考虑链接时效性和抓取解析速度相关问题
        # 然后入建哥的库
        return item

    def parseAndroid(self, response):
        item = UptodownItem()
        html_android = response.text
        item["android_html"] = html_android
        print("包含描述信息的页面", response.url)
        item["android_url"] = response.url
        # 这里调用解析，拿到下载地址，下载
        parse_result = self.__parseAndroid(html_android)
        for field in item.fields:
            if field in parse_result.keys():
                item[field] = parse_result[field]
        android_download_url = response.url + "/download"
        request = Request(android_download_url, callback=self.parseDownload, dont_filter=True)
        request.item = item
        yield request

    def parse(self, response):
        # # print("response.text", response.text)
        # html = response.text
        # parse_index(html)
        try:
            print("当前抓取的url为", response.url, )
            div = response.css(".app_card_tit")
            for url in div.css("a::attr(href)").extract():
                print("当前页面url", url)
                # redis 去重 只有不重复的任务才会被下发
                if not self.r.sismember("uptodown_app_set", url):
                    self.r.sadd("uptodown_app_set", url)
                    print(url)
                    yield Request(url, callback=self.parseAndroid, dont_filter=True)
        except:
            logging.info(traceback.format_exc())

        # finally:
        #     start_url = ['https://www.uptodown.com/android', "https://en.uptodown.com/android", ]
        #     for url in start_url:
        #         yield Request(url, dont_filter=True, priority=-1)

    @staticmethod
    def __parse_about(e):
        data_info = e(".data-info")("dd")
        data_len = data_info.__len__()
        print("data_len --> dd标签数量", data_len)

        language = e(".language .button-language").text()
        print("当前语言language为：({})".format(language))

        parse_data = {
            "app_size": 0,
            "app_publish_date": '2000-01-01',
            "app_developer": '',
            "app_download_capacity": 0,
        }
        for index, data in enumerate(data_info.items()):
            # print(index, data)
            if data_len == 13:
                if index == 7:
                    app_size = data.text()
                    parse_data["app_size"] = app_size
                elif index == 10:
                    # app 发布日期
                    # 7. "app_publish_date" app发布日期
                    publish_date = data(".right").text().replace("\n", "")
                    print("获得的原始发布d时间数据", publish_date)
                    date_list = publish_date.split(".")

                    if language == "cn" or language == "jp":
                        app_publish_date = publish_date.replace(".", "-")
                        parse_data["app_publish_date"] = app_publish_date
                    elif language == "id" or language == "kr" or language == "it" or language == "in" \
                            or language == "ru" or language == "br" or language == "de" \
                            or language == "es" or language == "fr" or language == "ar" or language == "th":
                        date_parse = [2, 1, 0]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                        parse_data["app_publish_date"] = app_publish_date
                    elif language == "tr":
                        # 兼容 16/05/18 格式的奇葩
                        date_list = publish_date.split("/")
                        date_parse = [2, 1, 0]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                        parse_data["app_publish_date"] = app_publish_date
                    else:
                        date_parse = [2, 0, 1]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                    parse_data["app_publish_date"] = app_publish_date
                    print('app_publish_date', app_publish_date)

                elif index == 5:
                    # 8. "app_developer" 'app开发商'
                    # app_developer = i('a').attr('href')
                    app_developer = data('a span').text()
                    parse_data["app_developer"] = app_developer
                    # print('app_developer', app_developer)
                elif index == 9:
                    # 9. app_download_capacity"  'app下载量'
                    app_download_capacity = data(".right").text().replace("\n", "")
                    parse_data["app_download_capacity"] = app_download_capacity
                    # print('app_download_capacity', app_download_capacity)

            elif data_len == 12:
                if index == 6:
                    app_size = data.text()
                    parse_data["app_size"] = app_size
                elif index == 9:
                    # app 发布日期
                    # 7. "app_publish_date" app发布日期
                    publish_date = data(".right").text().replace("\n", "")
                    print("获得的原始发布d时间数据", publish_date)
                    date_list = publish_date.split(".")

                    if language == "cn" or language == "jp":
                        app_publish_date = publish_date.replace(".", "-")
                        parse_data["app_publish_date"] = app_publish_date
                    elif language == "id" or language == "kr" or language == "it" or language == "in" \
                            or language == "ru" or language == "br" or language == "de" \
                            or language == "es" or language == "fr" or language == "ar" or language == "th":
                        date_parse = [2, 1, 0]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                        parse_data["app_publish_date"] = app_publish_date
                    elif language == "tr":
                        # 兼容 16/05/18 格式的奇葩
                        date_list = publish_date.split("/")
                        date_parse = [2, 1, 0]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                        parse_data["app_publish_date"] = app_publish_date
                    else:
                        date_parse = [2, 0, 1]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                    parse_data["app_publish_date"] = app_publish_date
                    print('app_publish_date', app_publish_date)
                elif index == 5:
                    # 8. "app_developer" 'app开发商'
                    # app_developer = i('a').attr('href')
                    app_developer = data('a span').text()
                    parse_data["app_developer"] = app_developer
                    # print('app_developer', app_developer)
                elif index == 8:
                    # 9. app_download_capacity"  'app下载量'
                    app_download_capacity = data(".right").text().replace("\n", "")
                    parse_data["app_download_capacity"] = app_download_capacity
                    # print('app_download_capacity', app_download_capacity)

            elif data_len == 11:
                # print(index, data)
                if index == 6:
                    app_size = data.text()
                    parse_data["app_size"] = app_size
                elif index == 8:
                    # app 发布日期
                    # 7. "app_publish_date" app发布日期
                    publish_date = data(".right").text().replace("\n", "")
                    print("获得的原始发布d时间数据", publish_date)
                    date_list = publish_date.split(".")

                    if language == "cn" or language == "jp":
                        app_publish_date = publish_date.replace(".", "-")
                        parse_data["app_publish_date"] = app_publish_date
                    elif language == "id" or language == "kr" or language == "it" or language == "in" \
                            or language == "ru" or language == "br" or language == "de" \
                            or language == "es" or language == "fr" or language == "ar" or language == "th":
                        date_parse = [2, 1, 0]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                        parse_data["app_publish_date"] = app_publish_date
                    elif language == "tr":
                        # 兼容 16/05/18 格式的奇葩
                        date_list = publish_date.split("/")
                        date_parse = [2, 1, 0]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                        parse_data["app_publish_date"] = app_publish_date
                    else:
                        date_parse = [2, 0, 1]
                        a, b, c = date_parse[0], date_parse[1], date_parse[2]
                        app_publish_date = "20{}-{}-{}".format(date_list[a], date_list[b], date_list[c])
                        print('app_publish_date 解析后的发布时间', app_publish_date)
                    parse_data["app_publish_date"] = app_publish_date
                    print('app_publish_date', app_publish_date)
                elif index == 4:
                    # 8. "app_developer" 'app开发商'
                    # app_developer = i('a').attr('href')
                    app_developer = data('a span').text()
                    parse_data["app_developer"] = app_developer
                    # print('app_developer', app_developer)
                elif index == 7:
                    # 9. app_download_capacity"  'app下载量'
                    app_download_capacity = data(".right").text().replace("\n", "")
                    parse_data["app_download_capacity"] = app_download_capacity
                    # print('app_download_capacity', app_download_capacity)

        # print(parse_data)
        return parse_data

    def __parseDownload(self, html, url):
        e = pq(html)
        meta = e.find('meta')
        # print('meta', meta)
        # print('type of meta', type(meta))

        # language
        language = e(".language .button-language").text()

        # 1.获取关键字
        # 这是一种比较讨巧的方法，它可以查找第 n 个 meta 标签
        key = meta('meta:nth-child(4)')
        keywords = key.attr('content')
        # print('key, keywords', key, keywords)

        # # 2.app名称
        app_name = e('.detail.name h1').text()
        # print('app_name', app_name)

        # 3.'app logo地址'
        info_img = e('.detail.icon')
        logo_url = info_img('img').attr('src')
        # print('logo_url', logo_url)

        # 4. 'app logo本地地址'
        # TODO: 这个没有下载，现在是空，记得指定
        logo_local_path = ''

        # 5. 'app包体大小'
        info_menu = e('.right_box ul dd')
        index = 1

        app_about = self.__parse_about(e)
        app_size = app_about.get("app_size")
        # 7. "app_publish_date" app发布日期
        app_publish_date = app_about.get("app_publish_date")
        # 8. "app_developer" 'app开发商'
        app_developer = app_about.get("app_developer")
        # 9. app_download_capacity"  'app下载量'
        app_download_capacity = app_about.get("app_download_capacity")

        # 6. "app_version" 'app版本号
        app_version = e('.version span').text()
        # print('app_version', app_version)

        # 10. "app_description" IS 'app描述信息
        short_desc = e('.short_desc').text()
        # print('app_description', app_description)

        # 11. "app_url" IS 'app详情页地址'
        app_url = url

        # 12. "apk_download_url" 'apk下载链接'
        apk_download_url = e('.data.download').attr('href')
        # print('apk_download_url', apk_download_url)
        # TODO: 这个下载链接好像会有时效性，时间久了会失效，跳转到apk详情页

        # 13. 'app第一级分类，例如：软件'
        app_category = ''
        # 14. "app_sub_category"  'app第二级分类，例如：系统工具';
        app_sub_category = ''

        navbar_wide = e('.navbar_wide')
        # print('navbar_wide', navbar_wide)
        breadcrumb = navbar_wide('.breadcrumb')
        span = breadcrumb('span')
        for index, s in enumerate(span.items()):
            # print(index, s.text())
            if index == 2:
                # 一级分类
                app_category = s.text()
            if index == 4:
                # 二级分类
                app_sub_category = s.text()

        # 15."app_detailed_category"  'app第三级分类，例如：优化';
        app_detailed_category = ''

        # 16. 是否需要翻墙
        fanqiang = False
        #
        # 17. 是否需要特殊请求头/cookie
        specialHeader = {
            "specialHeader": False,
            "header": {},
        }

        # 最终汇总
        app_info = {
            "uuid": str(uuid.uuid1()).replace('-', ''),
            "search_app_name": keywords,
            "app_name": app_name,
            "logo_url": logo_url,
            "logo_local_path": logo_local_path,
            "app_size": app_size,
            "app_version": app_version,
            "app_publish_date": app_publish_date,
            "app_developer": app_developer,
            "app_download_capacity": app_download_capacity,
            "short_description": short_desc,
            "app_url": app_url,
            "apk_download_url": apk_download_url,
            "app_category": app_category,
            "app_sub_category": app_sub_category,
            "app_detailed_category": app_detailed_category,
            "fanqiang": fanqiang,
            "specialHeader": specialHeader,
            "language": language,
        }
        return app_info

    def __parseAndroid(self, html):
        e = pq(html)
        description = e(".text-description")
        des = description.text().split("\n", 1)[-1]

        title = e(".name").text()
        # print(title.split("\n")[0])
        title_name = title.split("\n")[0]

        article = e(".article-content")
        # print(article)
        article_list = []
        for a in article.items():
            print(a)
            title = a("span").text()
            content = a("p").text()
            d = {
                "title": title,
                "content": content,
            }
            # print(d)
            article_list.append(d)
        d = {
            "title": title_name,
            "description": des,
            "description_article": article_list,
        }
        return d

    '''
    下面函数是入建哥库调用的
    '''

    def final_insert(self):
        pass

    @staticmethod
    def __data_to_send(mongo_info):
        """
        把需要插入 PostgreSQL 的数据拿到发给 redis
        :param mongo_info: 解析得到的数据
        """
        app_description = "{}\n{}".format(mongo_info.get("short_description"),
                                          mongo_info.get("description", ''))
        # try:
        app_download_capacity = mongo_info.get("app_download_capacity").replace(",", "")
        app_download_capacity = int(app_download_capacity)
        # 过度设计，一会删
        if app_download_capacity == "":
            app_download_capacity = 0
        # except Exception as e:
        #     raise Exception("app_download_capacity 有问题", mongo_info.get("app_url"), e)
        insert_info = {
            "uuid": mongo_info.get("uuid"),
            "search_app_name": mongo_info.get("app_name"),
            "app_name": mongo_info.get("app_name"),
            "logo_url": mongo_info.get("logo_url"),
            "logo_local_path": mongo_info.get("logo_local_path"),
            "app_size": mongo_info.get("app_size"),
            "app_version": mongo_info.get("app_version"),
            "app_publish_date": mongo_info.get("app_publish_date"),
            "app_developer": mongo_info.get("app_developer"),
            "app_download_capacity": app_download_capacity,
            "app_description": app_description,
            "channel_id": 1,
            "app_url": mongo_info.get("app_url"),
            "first_fetch_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "latest_fetch_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "apk_download_url": mongo_info.get("apk_download_url"),
            "app_category": mongo_info.get("app_category"),
            "app_sub_category": mongo_info.get("app_sub_category"),
            "app_detailed_category": mongo_info.get("app_detailed_category"),
            "app_unique_key": "",
        }
        return insert_info

    @staticmethod
    def get_value(info):
        """
        字符串拼接一下
            8684公交&14.3.0&应用宝&47&3D09F5260FF28BB7F2CAF0204B862C8E
            app_name app_version developer channel md5appurl
        :param info: 一个字典
        :return:
        """
        verify_list = [
            info.get("app_name"),
            info.get("app_version"),
            info.get("app_developer"),
            str(info.get("app_channel", 1)),
            md5(info.get("app_url")),
        ]
        value = "&".join(verify_list)
        return value

    def __sendRedis(self, info):
        """
        向redis发送一个队列 postgreSql_oversea_app_verify
        """
        value = self.get_value(info)
        redis_set_add(4, "postgreSql_oversea_app_verify", value)

    def __insert_app_info(self, info):
        """
        根据 data_clear_202， 插入 PostgreSQL t_app_info_overseas
        并且发送 redis 自校验， 发送redis给出search name
        """
        data_to_send = self.__data_to_send(info)
        # 查询redis 队列，是否存在该数据
        value = self.get_value(data_to_send)
        r = self.r7.sismember("s_app_info_repeat_overseas", value)
        if not r:
            # 新数据
            print("正在存入t_app_info_overseas，存入数据为：", data_to_send)
            try:
                self.app_info.insert_one(data_to_send)
                # 向redis 发送一个队列
                self.__sendRedis(data_to_send)
            except Exception as e:
                print("插入失败", e)

            # 再发送一次 redis 给出 search name
            name = info.get("app_name")
            # 判断 redis 里面是否已经有消息了
            self.r7.sadd("s_app_name_lite_overseas", name)

        else:
            print("数据已经存在", info)
