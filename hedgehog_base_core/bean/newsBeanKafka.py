import datetime
import json
import time


class NewsBeanKafka:
    """
    V0.3资讯 kafka结构体,最后维护时间2018/7/11,适用于JAVA/Python
    适用于资讯新闻、资讯视频
    python最终使用__dict__方法获得结构体输出
    etc:对其中图片/视频/缩略图Map进行说明
    {
      'url': '', #原图片/视频/缩略图 url
      'type': '', #格式后缀,比如图片填写jpg,视频填写mp4。
      'size': 0, #大小,使用字节数整形表达 比如32k就输入32768
      'fileUrl': '',#文件系统地址,要完整可达路径,比如http://172.10.3.161/group1/M00/2A/04/rAoDols9-aOAfP1xAADe3JVInDU4780792
      'videoLength':0 #如果是视频,则有视频长度,单位秒
    }

    """

    def __init__(self):
        # 时间相关
        self.createTime = int(time.time())  # [必填秒级时间戳]抓取时间
        self.publishDate = None  # [秒级时间戳]新闻发布时间
        # 新闻内容
        self.title = ""  # [必填字符串]标题(前后去除空格/无效字符)
        self.newsId = ""  # [必填字符串]抓取源新闻唯一ID

        self.video = None  # [必填字典/Map]视频video-url,没有视频用None/null代替,每个资讯只允许加载一个视频
        self.thumbnails = []  # [必填字典/Map-List]所有缩略图图片url,0-3个,没有缩略图用空list代替
        self.authorId = None  # [字符串]媒体/作者唯一ID(若抓取源无该id则用作者名填充)
        self.authorNickname = None  # [字符串]作者名
        self.introduce = None  # [长字符串]html原文,去除所有js标签和广告,视频就存储正文摘要
        # 抓取新闻特征
        self.url = ""  # [必填字符串]抓取页地址
        self.images = []  # [字典/Map-List]所有内容中图片url,没有图片用空list代替,不允许有None/null存在

        self.abstract = None  # [字符串]资讯摘要，按现有流逻辑可以省略摘要，视频的摘要直接写在introduce中

        self.videoReview = -1  # [int整型]抓取时视频弹幕数(不存在输入-1)
        self.collectionCount = -1  # [int整型]抓取时收藏数(不存在输入-1)
        self.commentCount = -1  # [int整型]抓取时评论数(不存在输入-1)
        self.praiseCount = -1  # [int整型]抓取时点赞数(不存在输入-1)
        self.badCount = -1  # [int整型]抓取时点踩数(不存在输入-1)
        self.readCount = -1  # [int整型]抓取时阅读数/播放量(不存在输入-1)
        self.transpondCount = -1  # [int整形]转发数(不存在输入-1)

        self.channel = None  # [字符串]频道标签/一级标签(只允许有一个)
        self.tags = None  # [字符串List]属性标签/二级标签
        # 补充新闻特征
        self.mediaType = None  # [必填整形int]新闻填写0,视频填写1
        self.fromType = None  # [必填整形int]代表抓取渠道(头条:0,前10都已使用2018/7/11,联系管理员领取)

        self.nlpTimes = None  # [字符串List]算法组补充的时间特征标签
        self.nlpLocations = None  # [字符串List]算法组补充的地域特征标签
        self.manualNum = None  # [字典/Map]人工筛选标签,默认为None
        # 其他
        self.etc = None  # [字典/Map]其他记录,其中log这个key保留记录错误信息,其他随意使用
        self.content = None  # [不用填写]新闻标签过滤后的正文
        self.searchWord = None  # [不用填写]你的抓取来源位置


def getTestNewsBean():
    print("测试:示范如何组装一个News结果(方便你偷懒复制使用)")
    print("范例1:头条资讯《作死！司法平台上悔拍 男子被法院强制转账280万》")
    newsBean = NewsBeanKafka()
    # 时间相关
    newsBean.createTime = int(time.time())  # [必填秒级时间戳]抓取时间
    """
    从指定字符串格式转化为秒级时间戳
    """
    dPublish = datetime.datetime.strptime("2018-06-01 09:51:06", '%Y-%m-%d %H:%M:%S')
    newsBean.publishDate = int(dPublish.timestamp())
    # 新闻内容
    newsBean.title = "作死！司法平台上悔拍 男子被法院强制转账280万"
    newsBean.newsId = "6561927770719404557"
    thumbnail1 = {'url': 'http://5b0988e595225.cdn.sohucs.com/images/20180704/02b662e39ae94171b6ecde54132d25dd.jpeg', 'type': 'jpeg', 'size': 34181, 'fileUrl': 'http://172.10.3.161/group1/M00/22/DB/rAoDols9zkeAZcdOAACFhdE0uXQ0480065'}
    thumbnail2 = {'url': 'http://5b0988e595225.cdn.sohucs.com/images/20180704/03a4bcd13cf44f6daf2067ca7e0e2423.jpeg', 'type': 'jpeg', 'size': 44722, 'fileUrl': 'http://172.10.3.161/group1/M00/22/DC/rAoDols9zkiAAhLyAACusglsK-82313996'}
    newsBean.thumbnails = [thumbnail1, thumbnail2]
    # 没有额外需求的图片不需要存储
    newsBean.authorId = '50502346296'  # [字符串]媒体/作者唯一ID(若抓取源无该id则用作者名填充)
    newsBean.authorNickname = '中国经济网'  # [字符串]作者名
    newsBean.introduce = r"""
    <p>2016年5月，南通中院在南通九舜船务工程有限公司与南通尧盛钢结构有限公司买卖合同纠纷案中，根据申请，将被执行人纳入失信名单。随后，法院依法查封了被执行人位于通州区的一处房地产及附属设施、机器设备等，因被执行人一直未自觉履行生效法律文书确定的义务，申请人向法院申请强制拍卖、变卖上述资产用以清偿债务。在2017年8月24号至8月25日的拍卖中，上述资产受到较为热烈的追捧。淘宝网司法拍卖平台页面显示，当时4名竞买人从1091.45万元开始起拍，一路加价。</p>
<img data-original="http://p3.pstatp.com/large/pgc-image/15278178597371659114f2d" width="583" height="328" alt="作死！司法平台上悔拍 男子被法院强制转账280万" inline="0">
<img data-original="http://p1.pstatp.com/large/pgc-image/1527817862733f84b7e771f" width="583" height="328" alt="作死！司法平台上悔拍 男子被法院强制转账280万" inline="0">
<p>南通中级法院执行局法官助理郭伟：经过了90轮的竞价，87次延时，最终以1840多万的价格成交，竞买人浦某拒不缴余款，虽然我们法院多次催促，他还是未缴。</p>
<img data-original="http://p9.pstatp.com/large/pgc-image/152781786394549e496d1ab" width="583" height="328" alt="作死！司法平台上悔拍 男子被法院强制转账280万" inline="0">
<p>随后，法院于2017年12月11日至12日在同一平台对上述资产重新拍卖，另一竞买人最终以1566.45万元竞得，且将拍卖款全额汇入法院账户。两次拍卖金额相差280万元。</p><p>南通中级法院执行局法官助理郭伟： 对浦某的这种悔拍行为，根据最高人民法院关于人民法院民事执行中拍卖变卖财产的规定，一个是100万保证金的没收，另外是180万差额责令他向法院缴纳。</p>
<img data-original="http://p1.pstatp.com/large/pgc-image/15278178614319385491a93" width="583" height="328" alt="作死！司法平台上悔拍 男子被法院强制转账280万" inline="0">
<p>据了解，浦某并未自觉补交剩下的180万元，法院冻结了浦某名下银行存款180万元，并强制划至法院账户。</p>
<p>南通中级法院执行局法官助理郭伟：要在淘宝网上参与竞拍司法拍卖标的物，一定要充分了解标的物，另外一定要有一个自己的心理价位，不要盲目跟风，不要盲目竞拍，悔拍，不想再要这个东西了，是要承担相应的法律责任的。</p>
<p>（视频来源：南通新闻）</p>
    """
    # 抓取新闻特征
    newsBean.url = "https://www.toutiao.com/a6561927770719404557/"  # [必填字符串]抓取页地址

    newsBean.commentCount = 0  # [int整型]抓取时评论数(不存在输入-1)
    newsBean.praiseCount = -1  # [int整型]抓取时点赞数(不存在输入-1)
    newsBean.badCount = -1  # [int整型]抓取时点踩数(不存在输入-1)
    newsBean.readCount = -1  # [int整型]抓取时阅读数(不存在输入-1)
    newsBean.channel = '体育'  # [字符串]频道标签/一级标签(只允许有一个)
    newsBean.tags = ['法律', '郭伟', '法制', '社会']  # [字符串List]属性标签/二级标签
    # 补充新闻特征
    newsBean.mediaType = 0  # [必填整形int]新闻填写0,视频填写1
    newsBean.fromType = 0  # [必填整形int]代表抓取渠道(头条:0,前10都已使用2018/7/11,联系管理员领取)
    # 其他
    newsBean.etc = {'msg': '测试数据'}  # [字典/Map]其他记录,其中log这个key保留记录错误信息,其他随意使用
    return newsBean


def getTestVideoBean():
    print("测试:示范如何组装一个Video结果(方便你偷懒复制使用)")
    print("范例2:BiliBili影片《不愧是票房冠军!这个视频告诉你《捉妖记2》到底值不值得看!》")
    newsBean = NewsBeanKafka()
    # 时间相关
    newsBean.createTime = int(time.time())  # [必填秒级时间戳]抓取时间
    """
    从指定字符串格式转化为秒级时间戳
    """
    dPublish = datetime.datetime.strptime("2018-02-27 16:32:43", '%Y-%m-%d %H:%M:%S')
    newsBean.publishDate = int(dPublish.timestamp())
    # 新闻内容
    newsBean.title = "不愧是票房冠军!这个视频告诉你《捉妖记2》到底值不值得看!"
    newsBean.newsId = "av20131777"
    videoDict = {'url': 'http://www.bilibili.com/video/av20131777', 'type': 'flv', 'size': 149857, 'fileUrl': 'http://172.10.3.161/group1/M00/A0/1D/rAoDols6ArOAe0g8AAJJYTsnKXs482.flv'}
    newsBean.video = videoDict
    # 没有缩略图不需要存储
    newsBean.thumbnails = []
    newsBean.authorId = '不可名状酱'  # [字符串]媒体/作者唯一ID(若抓取源无该id则用作者名填充)
    newsBean.authorNickname = '不可名状酱'  # [字符串]作者名
    # 抓取新闻特征
    newsBean.url = "http://www.bilibili.com/video/av20131777"  # [必填字符串]抓取页地址

    newsBean.commentCount = 156  # [int整型]抓取时评论数(不存在输入-1)
    newsBean.praiseCount = -1  # [int整型]抓取时点赞数(不存在输入-1)
    newsBean.badCount = -1  # [int整型]抓取时点踩数(不存在输入-1)
    newsBean.readCount = 5592  # [int整型]抓取时阅读数(不存在输入-1)
    newsBean.channel = '搜索'  # [字符串]频道标签/一级标签(只允许有一个)
    newsBean.tags = ['日常']  # [字符串List]属性标签/二级标签
    # 补充新闻特征
    newsBean.mediaType = 1  # [必填整形int]新闻填写0,视频填写1
    newsBean.fromType = 10  # [必填整形int]代表抓取渠道(头条:0,前10都已使用2018/7/11,联系管理员领取)
    # 其他
    newsBean.etc = {'search_keyword': '捉妖记2', 'msg': '测试数据'}  # [字典/Map]其他记录,其中log这个key保留记录错误信息,其他随意使用
    return newsBean


if __name__ == '__main__':
    newsBean1 = getTestNewsBean()
    newsBean2 = getTestVideoBean()
    jsonStr1 = json.dumps(newsBean1.__dict__)
    jsonStr2 = json.dumps(newsBean2.__dict__)
    print(newsBean1)
    print(newsBean2)
