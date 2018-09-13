import datetime


class NewsBean:
    def __init__(self):
        # 创建时间
        self.createTime = datetime.datetime.now()  # (Date)创建时间,初始化的时候自动生成
        """
        新闻内容属性
        """
        self.url = ''  # (string)新闻落地页地址
        self.newsId = ''  # (string)新闻ID
        self.titleInfo = ''  # (string)标题
        self.content = ''  # (string)正文html
        self.publishDate = datetime.datetime.now()  # (Date)新闻资讯创作时间
        self.introduction = ''  # (string)新闻摘要
        self.tags = []  # (list[string])tags队列，二级标签
        self.images = []  # [字典/Map-List]所有内容中图片url,没有图片用空list代替,不允许有None/null存在
        self.thumbnails = []  # (list[string])图片url列表
        """
        对from类标签举例说明。
        现在假设有一个场景，从今日头条的推荐流中抓取了一个体育的新闻
        fromType=1(从克南处获取,头条抓取=1)
        fromChannel=体育
        fromSpider=推荐流
        """
        self.fromType = 0  # (int)新闻类型,从克南处获取
        self.fromChannel = ''  # (string)一级标签，例如 世界杯
        self.fromSpider = ''  # (string)抓取该文章的时候所在的频道
        """
        作者信息,没有作者ID的直接使用作者姓名当ID
        """
        self.mediaName = ''  # (string)作者（媒体）姓名
        self.mediaId = ''  # (string)作者（媒体）ID，没有作者ID的直接使用作者姓名当ID
        """
        统计信息
        五个统计数据,不存在存储-1,必须存储int类型
        """
        self.readNum = -1  # (int)阅读数
        self.commentNum = -1  # (int)评论数
        self.goodNum = -1  # (int)点赞数
        self.unlikeNum = -1  # (int)不喜欢数
        self.shareNum = -1  # (int)分享数
        self.collectionCount = -1  # (int)收藏数
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
        self.imgFileUrls = []
        self.videoFileUrls = []
        """
        其他
        """
        self.etc = {}  # dict 其他要存储的东西,主要是测试相关和调试中间信息
