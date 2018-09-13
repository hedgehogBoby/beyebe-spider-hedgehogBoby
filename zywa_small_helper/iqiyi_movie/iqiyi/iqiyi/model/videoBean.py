import datetime


class VideoBean:
    def __init__(self):
        # 影片信息
        self.videoId = ''  # 影片id
        self.description = ''  # 影片描述
        self.areas = []  # 发布地区列表
        self.language = ''  # 语言
        self.url = ''  # 落地页url
        self.runtime = 0  # 电影长度秒
        # 主演\导演\编剧
        self.writers = []
        self.directors = []
        self.mainActors = []
        # 分类标签
        self.category = ''  # 一级标签
        self.tags = []  # 二级标签
        self.keywords = []  # 更多关键词，可能会有有配音语种、地区、规格、类型、题材等
        # 时间信息
        self.uploadDate = None
        self.publishDate = None
        # 其他
        self.isVip = 0
        self.etc = {}
        self.etc2 = {}
        # tid和vid
        self.technologyMsg = {}
        # 图片,共有6个尺寸可供选择，并且存储进文件系统
        self.imgs = []  # ['_180_236', '_440_608', '_480_270', '_260_360', '_180_236', '_1080_608']
