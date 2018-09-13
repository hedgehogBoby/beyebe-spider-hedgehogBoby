
import traceback
from zywa_database_core.dao.redis.redisTest import redisSelectAll3
from zywa_download_httpserver.helper.annie.annieDownloadVideo import AnnieDownloadVideo
from zywa_download_httpserver.impl.request.fileImpl import FileImpl
from zywa_scrapy_download.scrapy_download.scrapy_download.helper.webDriverPhantomJSHelper import webDriverPhantomJSGet

if __name__ == '__main__':
    print('你好,正在进行【小刺猬下载集群】搭建环境自检！')
    # 数据库自检

    print("[Warning]尚未开发mongo数据库自检功能")
    # redis/IP池自检

    keyCheakTitle = 'redis/ip池'
    print("正在进行{}自检".format(keyCheakTitle))
    try:
        content = redisSelectAll3('ippool')
        print(content)
        print('[SUCCESS]{}自检成功'.format(keyCheakTitle))
    except:
        print('[ERROR]{}自检失败'.format(keyCheakTitle))
        traceback.print_exc()

    # WebDriver自检

    keyCheakTitle = 'WebDriver'
    print("正在进行{}自检".format(keyCheakTitle))
    try:
        content = webDriverPhantomJSGet("http://www.baidu.com")
        print(content[0:10])
        print('[SUCCESS]{}自检成功'.format(keyCheakTitle))
    except:
        print('[ERROR]{}自检失败'.format(keyCheakTitle))
        traceback.print_exc()

    """
    Scrapy自检
    """

    print('[WARNING]暂时不支持Scrapy自检,请输入pip3 install scrapy')

    """
    文件系统自检
    """

    keyCheakTitle = '文件系统'
    print("正在进行{}自检".format(keyCheakTitle))
    try:
        content = FileImpl('/Users/magic/PycharmProjects/zywa-spider-xiaociwei/zywa_test_others/cheakMyself').fileToFileSystem('testFile.txt', 1)
        print(content)
        print('[SUCCESS]{}自检成功'.format(keyCheakTitle))
    except:
        print('[ERROR]{}自检失败'.format(keyCheakTitle))
        traceback.print_exc()
    """
    Anine自检
    """
    keyCheakTitle = 'annie'
    print("正在进行{}自检".format(keyCheakTitle))
    try:
        content = AnnieDownloadVideo('https://www.bilibili.com/video/av22109582?from=search&seid=10249235518781595878', '').downloadVideo()
        print(content)
        print('[SUCCESS]{}自检成功'.format(keyCheakTitle))
    except:
        print('[ERROR]{}自检失败'.format(keyCheakTitle))
        traceback.print_exc()
