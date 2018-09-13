import threading
import traceback

import requests
import time

from multiprocessing import Process

successNum = 0
errNum = 0
totalNum = 0


def download():
    global successNum, errNum, totalNum
    # 请求网址
    # 【前端】直接返回文件，不再解析
    url = 'http://172.10.3.43:4540/fastdfs?type=download&id=group2/M00/47/E7/rAoDIVraur-AGegLAC7FHJY159E1594581&style=image'
    # 发起请求，下载文件
    try:
        requests.get(url)
        # 返回的文件信息是str类型，需要转成dict类型   {'Remote file_id': b'group1/M00/55/E4/rAoDIFrZon-AXWvWAAADbtrz9fU5496126', 'Content': b'\x89PNG\r\82', 'Download size': '878B', 'Storage IP': b'172.10.3.32'}
        successNum = successNum + 1
        print("success")
    except:
        errNum = errNum + 1
        traceback.print_exc()
    finally:
        totalNum = totalNum + 1


def upload(files):
    global errNum, totalNum
    # 请求网址
    url = 'http://172.10.3.43:4540/fastdfs?type=upload'
    # 上传网页
    # uploadFile = requests.get("https://www.baidu.com/",verify=False).content
    try:
        # 发起请求，上传文件
        response = requests.post(url, files=files)
        # 返回的文件信息是str类型，需要转成字典    {'Group name': b'group1', 'Remote file_id': b'group1/M00/55/E4/rAoDIFrZo', 'Status': 'Upload successed.', 'Local file name': '', 'Uploaded size': '878B', 'Storage IP': b'172.10.3.32'}
        print("success totalNum :" + str(totalNum - errNum))
        totalNum = totalNum + 1
        print(response.text)
        return response.text
    except:
        print("err errorNum :" + str(errNum))
        errNum = errNum + 1
        return None


def test():
    global errNum, totalNum
    while True:
        # upload(files)
        download()


if __name__ == '__main__':
    # with open('/Users/magic/PycharmProjects/zywa-spider-xiaociwei/img/readme/代码实现结构.JPG', 'rb') as f:
    #     files = {'file': f.read()}
    # dictStr = upload(files)
    # dict = strToObj(dictStr)
    # print(dict['Remote file_id'])
    for i in range(100):
        print("已启动进程:" + str(i))
        Process(target=test, args=()).start()

    # while True:
    #     print(str(errNum) + ':' + str(successNum) + ':' + str(totalNum))
    #     time.sleep(0.01)
