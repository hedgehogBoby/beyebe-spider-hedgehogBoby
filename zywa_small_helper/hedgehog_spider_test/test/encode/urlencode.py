from urllib.parse import quote

if __name__ == '__main__':
    '''
        钓鱼视频搜狗搜索页
    '''
    ip = 'localhost'
    # ip = '172.10.3.103'
    searchKey = quote('钓鱼视频')
    print(searchKey)
    url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={searchKey}&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=2784&sst0=1522286025307&lkt=1%2C1522286025201%2C1522286025201'.replace('{searchKey}', searchKey)
    url_head = 'http://{ip}:4569/extract/ippool/webdriver/xml.go?url='.replace('{ip}', ip)
    urlNow = url_head + quote(url)
    print('钓鱼视频搜狗搜索页: ' + urlNow)

    url = 'http://mp.weixin.qqVideo.com/s?src=3&timestamp=1522375400&ver=1&signature=a*MVsFDBygtQH3CBQkLUTJML-i5DiBJHKEX7Tt5XFs0hur02X8r6wRUXKiX8ntl85WOQG56QQfxvvNTMwkt6gS6DZfOg*zNIOAGcHTAwYWv8POxySUk7nc*mlcQhJdudL6oI0cCmDQYqSEugKixwwx4ltIKAwLCy6REoIjQJ0xM='
    url_head = 'http://{ip}:4569/extract/ippool/webdriver/xml.go?url='.replace('{ip}', ip)
    urlNow = url_head + quote(url)
    print('视频搜内容页: ' + urlNow)

    # 编码问题
    url = 'http://www.chinasafety.gov.cn/index.shtml'
    url_head = 'http://{ip}:4568/extract/ippool/xml.go?url='.replace('{ip}', ip)
    urlNow = url_head + quote(url)
    print('编码错误内容页: ' + urlNow)


