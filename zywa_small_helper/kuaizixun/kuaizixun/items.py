# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KuaizixunItem(scrapy.Item):
    # 创建时间  # (Date)创建时间,初始化的时候自动生成
    createTime = scrapy.Field()
    """
    新闻内容属性
    """
    url = scrapy.Field()               # (string)新闻落地页地址
    newsId = scrapy.Field()            # (string)新闻ID
    titleInfo = scrapy.Field()         # (string)标题
    content = scrapy.Field()           # (string)正文html
    publishDate = scrapy.Field()       # (Date)新闻资讯创作时间
    introduction = scrapy.Field()      # (string)新闻摘要
    tags = scrapy.Field()              # (list[string])tags队列
    imgUrls = scrapy.Field()           # (list[string])图片url列表

    """
    对from类标签举例说明。
    现在假设有一个场景，从今日头条的推荐流中抓取了一个体育的新闻
    fromType=1(从克南处获取,头条抓取=1)
    fromChannel=体育
    fromSpider=推荐流
    """
    fromType = scrapy.Field()          # (int)新闻类型,从克南处获取
    fromChannel = scrapy.Field()       # (string)channel 例如世界杯
    fromSpider = scrapy.Field()        # (string)抓取该文章的时候所在的频道
    """
    作者信息
    """
    mediaName = scrapy.Field()         # (string)作者（媒体）姓名
    mediaId = scrapy.Field()           # (string)作者（媒体）ID

    """
    统计信息
    五个统计数据,不存在存储-1,必须存储int类型
    """
    readNum = scrapy.Field()           # (int)阅读数
    commentNum = scrapy.Field()        # (int)评论数
    goodNum = scrapy.Field()           # (int)点赞数
    unlikeNum = scrapy.Field()         # (int)不喜欢数
    shareNum = scrapy.Field()          # (int)分享数
    """
    需要爬虫组额外下载的资源
    key:图片/视频 url
    value:文件系统信息
    {
      fileUrl:文件系统完整地址,例:
      imgType:存储文件格式,例:jpeg
      fileSize:文件大小,以字节单位存储int
    }
    """
    imgFileUrls = scrapy.Field()
    videoFileUrls = scrapy.Field()
    """
    其他
    """
    etc = scrapy.Field()              # dict 其他要存储的东西,主要是测试相关和调试中间信息






