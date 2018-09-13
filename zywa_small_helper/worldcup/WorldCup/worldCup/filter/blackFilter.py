blackList = [
    '（搜狐体育独家出品 未经许可严禁转载）',
    '返回搜狐，查看更多',
    '声明：该文观点仅代表作者本人，搜狐号系信息发布平台，搜狐仅提供信息存储空间服务。',
    '网易体育',
    '搜狐体育',
    '新浪体育',
    '责任编辑：'
]

blackUrlList = [
    'photoview'
]


def filterContent(content):
    for i in blackList:
        content = content.replace(i, '')
    return content


def isFilterUrl(url):
    for i in blackUrlList:
        if i in url:
            return True
    return False
