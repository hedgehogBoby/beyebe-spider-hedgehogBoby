# -*- coding: utf-8 -*-
# Created on 2018/3/22


import os
from urllib.parse import urlparse

import requests

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15"}


def download(url, fileName):
    global headers
    all_content = requests.get(url, headers=headers).text  # 获取M3U8的文件内容
    # file_line = all_content.split("\r\n")  # 读取文件里的每一行
    file_line = all_content.split("\n")  # 读取文件里的每一行
    # 通过判断文件头来确定是否是M3U8文件
    print(file_line[0])
    if file_line[0] != "#EXTM3U":
        raise BaseException(u"非M3U8的链接")
    else:
        for index, line in enumerate(file_line):
            if '.m3u8' in line:
                parsed_tuple = urlparse(url, fileName)
                print(parsed_tuple)
                pd_url = parsed_tuple[0] + '://' + parsed_tuple[1] + line
                download2(pd_url, fileName)
                print("下载真的完成")


def download2(url, fileName):
    download_path = "/Users/magic/PycharmProjects/zywa-spider-xiaociwei/zzshell/webdriver"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text  # 获取M3U8的文件内容
    file_line = all_content.split("\n")  # 读取文件里的每一行
    # 通过判断文件头来确定是否是M3U8文件
    if file_line[0] != "#EXTM3U":
        raise BaseException(u"非M3U8的链接")
    else:
        unknow = True  # 用来判断是否找到了下载的地址
        for index, line in enumerate(file_line):
            if "EXTINF" in line:
                unknow = False
                # 拼出ts片段的URL
                pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]
                res = requests.get(pd_url)
                c_fule_name = fileName
                with open(download_path + "/" + c_fule_name, 'ab') as f:
                    f.write(res.content)
                    f.flush()
        if unknow:
            raise BaseException("未找到对应的下载链接")
        else:
            print("下载完成")


if __name__ == '__main__':
    url = "http://bf.ahpai.cc/20180715/c9D4UA7s/index.m3u8"

    download(url, 'testMovie.m3u8')
