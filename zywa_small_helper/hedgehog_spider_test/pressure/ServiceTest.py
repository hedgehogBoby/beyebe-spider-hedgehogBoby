import json
import traceback

import requests

from zywa_download_httpserver.model.actionBeanList import ActionBeanList


def xiaociweiTest():
    global timeout
    print("接下来将会全面对服务做一次TEST by XiaoCiWei")
    # -------------------------------------------------------

    urlBase = 'http://{}/extract/xml.go?isProxy=1&url=https%3A//www.baidu.com'
    # urlBase = 'http://{}/test.go'
    # urlBase = 'http://{}/extract/xml.go?isProxy=0&url=http://ipinfo.io/ip'
    actionBeanList = ActionBeanList()
    actionBeanList.appendActionBean(name='waitfor', msg='<h3', timeout=5)
    textStr = '西城区国土局'
    # -------------------------------------------------------
    ipList = ['172.10.3.103:4564', '172.10.3.102:4564', '172.10.3.101:4564']
    # ipList = ['58.87.72.133:4565',
    #           '58.87.89.196:4565',
    #           '211.159.154.149:4565',
    #           '123.206.57.75:4565',
    #           '111.231.86.180:4565',
    #           '115.159.124.97:4565',
    #           '119.29.111.183:4565',
    #           '139.199.161.64:4565',
    #           '172.10.3.101:4565']
    timeout = 30
    myHeaders = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.1; OS105 Build/NMF26X) NewsArticle/6.6.2 okhttp/3.7.0.6'}
    # -------------------------------------------------------

    print("IP检测池共有IP数量:" + str(len(ipList)))
    i = 0
    for ipNow in ipList:
        i = i + 1
        print(str(i) + " ip:" + ipNow)
        try:
            urlBaseNow = urlBase.format(ipNow)
            print('测试地址:' + urlBaseNow)
            html = __httpGetTest(urlBaseNow, myHeaders, actionBeanList)
            if textStr == 'test':
                print(html)
            else:
                if textStr in html:
                    print('test success!exist str')
                else:
                    print('test failed,No str\n' + html)
        except Exception as err:
            print('test failed,Exception:' + str(err))


def __httpGetTest(urlNow, myHeaders, actionBeanList):
    global timeout
    s = requests.session()
    myHeaders.update({'action': actionBeanList.getJSONString()})
    try:
        if myHeaders is not None:
            response = s.get(urlNow, headers=myHeaders, verify=False, timeout=timeout)
        else:
            response = s.get(urlNow, verify=False, timeout=timeout)

        response.encoding = "utf-8"

        return response.text
    finally:
        s.close()


if __name__ == '__main__':
    xiaociweiTest()
