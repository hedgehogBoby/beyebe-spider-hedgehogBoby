#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17
# @Author  : admin
import base64
import hashlib
import importlib
import re
from urllib import parse
from urllib.parse import urlparse
from urllib import request

import datetime
from bs4 import BeautifulSoup

import requests
from chardet import UniversalDetector


def _partition(entity, sep, isright=False):
    if isright:
        # 从右开始分割
        parts = entity.rsplit(sep, 1)
    else:
        parts = entity.split(sep, 1)

    if len(parts) == 2:
        return parts[0], sep, parts[1]
    else:
        return entity, '', ''


def parse_db_connect_url(connect_url):
    """
    解析数据库连接 connect_url
    :param connect_url:
    :return:解析出的信息
    """
    result_parse = {}
    url_parse = urlparse(connect_url)
    if url_parse.scheme:
        result_parse['dbtype'] = url_parse.scheme

    if url_parse.path and url_parse.path != '/':
        result_parse['database'] = url_parse.path.replace('/', '')

    if url_parse.query:
        result_parse['query'] = url_parse.query

    if url_parse.netloc:
        user, _, address = _partition(url_parse.netloc, '@')

        # 默认优先获取 host,port
        if user and not address:
            address, user = user, address

        if user:
            username, _, password = _partition(user, ':')

            # 密码可能为空
            if username or password:
                result_parse['username'] = username
                result_parse['password'] = password

        if address:
            host, _, port = _partition(address, ':')

            if host:
                result_parse['host'] = host
            if port:
                result_parse['port'] = port

    return result_parse


def distinct_list(source_list):
    # list 去重
    return list(set(source_list))


def url_join(base, url):
    """
    url 自动补全
    :param base:基础url ，需 http:|https 开头
    :param url:待拼接部分
    :return:完成拼接url
    print(url_join('http://www.39693.cn/app/soft/', '/app/26459.html'))
    """
    return request.urljoin(base, url)


def import_config(name):
    """
    导入配置文件
    :param name: 配置文件名
    :return: conf 字典
    """
    config = {}
    module = importlib.import_module(name)
    for key in dir(module):
        if key.isupper():
            config[key] = getattr(module, key)
    # todo 自动添加业务名
    return config


def import_dynamic_func(conf):
    """
    动态加载方法
    :param conf:
    :return:
    """
    func = None
    if conf:
        module_name, _, func_name = _partition(conf, '.', True)
        module = importlib.import_module(module_name)
        func = {}
        if func_name in dir(module):
            func[func_name] = getattr(module, func_name)
    return func


def extract_apk(html):
    """
    根据html，抽取apk
    :param html:
    :return:
    """
    # apk_regex = re.compile(r"(?:(?:href\s*=\s*|src[\s]*=[\s]*|window.location.href=)(?:\"|\')){0,1}((?:http|https|www|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\.|/){0,1}[\S]*?\.apk)")
    # apk_regex = re.compile(
    #     r"(?:(?:href\s*=\s*|src[\s]*=[\s]*|location.href=|location.href=)(?:\"|\')){0,1}((?:http|https|www|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\.|/){0,1}[\S]*?\.apk)")
    html = del_html_text(html)

    apk_regex = re.compile(
        r"(?:\"|\'){1,2}((?:http|https|www|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\.|/){0,1}[\S]*?\.apk)")
    apk_regex2 = re.compile(r"(?:(?:href\s*=\s*|src[\s]*=[\s]*)(?:\"|\'))([\S]*?\.apk)")
    extract_info = re.findall(apk_regex, html)
    if extract_info.__len__() == 0:
        extract_info = re.findall(apk_regex2, html)

    # print('extract_info', new_extract_info)
    # 处理存在多个"/'的情况
    new_extract_info = []
    for apk_info in extract_info:
        for i in range(10):
            check_apk = re.findall(apk_regex, apk_info)
            if check_apk.__len__() > 0:
                apk_info = check_apk[0]
            else:
                break
        new_extract_info.append(apk_info)
    return new_extract_info


def extract_gov_info(html):
    """
    从主页抽取政府单位信息
    :param html:
    :return:
    """
    # (?:"){0,1}
    info_regex = re.compile(
        r'(?:href\s*=\s*"|onclick="){0,1}(?:window.open\((?:\'|\")){0,1}([\S]*?bszs.conac.cn/sitename[\S]+?)(?:\"|\')')
    # info_regex = re.compile(r'(bszs.conac.cn/sitename[\S]*?)"')

    extract_info = re.findall(info_regex, html)
    extract_url = ''
    if extract_info.__len__() > 0:
        extract_url = extract_info[0]
        print(extract_url)
        extract_url = url_join('http://bszs.conac.cn', extract_url)
    return extract_url


def url_encode(url):
    """
    urlencode
    :param url:
    :return:
    """
    return parse.quote_plus(url)


def get_qrcode_info(analyze_obj, url):
    """
    获取二维码信息
    """
    url = url_encode(url)
    # print('print', analyze_obj)
    try:
        resp = requests.get('http://172.10.3.101:4567/utils/qrcode/url.go?url={0}'.format(url), timeout=30)
        print('url:{0} 请求返回:{1}'.format(url, resp.text))
        if 'data' in resp.json().keys():
            analyze_obj['qrcode_url'].extend(resp.json()['data'])
        # return
        return analyze_obj
    except Exception as exce:
        print('url:{0} 请求异常:{1}'.format(url, exce))
        return None


def get_info(resptext):
    """
    提取政府网站信息
    """
    try:
        soup = BeautifulSoup(resptext)
        table_soup = soup.find_all('table')
        tr_soup = table_soup[0].find_all('tr')
        info_dict = {}
        for tr in tr_soup:
            td_soup = tr.find_all('td')
            if len(td_soup) == 2:
                info_dict[td_soup[0].text.strip()] = td_soup[1].text.strip()
            else:
                info_dict[td_soup[0].text.strip()] = ''
    except Exception as exce:
        print('resptext', resptext)
        print(exce)
        return {}

    return info_dict


def get_gov_dict(apk_dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    tld = apk_dict['tld']
    try:
        resp = requests.get(tld, headers=headers, verify=False)
        gov_info_url = extract_gov_info(resp.text)
        if gov_info_url:
            apk_dict['info'] = gov_info_url
            resp = requests.get(gov_info_url, headers=headers, verify=False)
            apk_dict['dict'] = get_info(resp.text)
        else:
            apk_dict['info'] = ''
    except Exception as exce:
        print(exce)
    return apk_dict


def now_date_str(format='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间，字符串
    """
    return datetime.datetime.now().strftime(format)


def extract_html_text(html):
    """
    提取html中的文本信息
    :param html:
    :return:
    """
    p = re.compile('<[^>]+>')  # 提取文本
    return p.sub("", html)


def del_html_text(html):
    """
    删除html中的文本信息
    提取apk时，注意不能删除script中的信息
    todo 因为会删除script信息，当前版本，文本中有换行则不过滤
    :param html:
    :return:
    """
    # p = re.compile('>(.+?)<')
    # p = re.compile('>[^<\s]+?<')
    p = re.compile('>[^<\s]+?<')
    return p.sub("><", html)


def df_insert_mongo(df, connect_url, table):
    """
    dataframe 插入 mongo数据库
    :param df:待插入dataframe
    :param connect_url:
    'mongodb://172.10.3.157/lichangjian'
    'mongodb://127.0.0.1/lichangjian'
    :param table:
    :return:
    """
    from db.mongo_helper import MongoHelper
    client = MongoHelper(connect_url=connect_url)
    table = client.mongo_database[table]
    datas = df.to_dict('records')
    return table.insert_many(datas)


def get_table_column_name(table):
    """
    获取数据库列表
    :param table:
    :return:
    """
    # todo 移至数据库操作内
    import psycopg2
    conn = psycopg2.connect(database="db_app", user="postgres", password="123456", host="172.10.3.170",
                            port="5432")
    cur = conn.cursor()
    sql = 'select * from {0} limit 1'.format(table)
    cur.execute(sql)
    return [desc.name for desc in cur.description]


def md5_encode(source_str):
    """
    md5 加密
    :param source_str:
    :return:
    """
    m = hashlib.md5()
    m.update(source_str.encode("utf-8"))
    return m.hexdigest().upper()


def base64_encode(source_str):
    """
    base64加密
    :param source_str:
    :return:
    """
    bs64 = base64.b64encode(source_str.encode('utf-8'))
    return bs64.decode('utf-8')


# print(base64_encode('demo&demo'))


def extract_date_re(date_str):
    """
    提取时间正则
     '更新时间:2014/7/30 9:44:55'
    :param date_str:
    :return:
    """
    regex = re.compile(
        "(?:\\d{4})(?:/|-|\.)(?:\\d{1,2})(?:/|-|\.)(?:\\d{1,2})(?:(?:\s{0,1}\\d{1,2}[\s:]\\d{1,2}[\s:]\\d{1,2})){0,1}")
    result = re.findall(regex, date_str)
    if len(result) >= 1:
        return result[0]
    else:
        return ''


def extract_info_re(source_str):
    """
    提取标签信息
    '更新时间:2014/7/30 ' 中 ：后部分
    :param source_str:
    :return:
    """
    regex = re.compile('[\w\d/./-]+')
    result = re.findall(regex, source_str)
    if len(result) >= 2:
        return result[1]
    else:
        return ''


def extract_version(source_str):
    """
    提取版本信息
    :param source_str:
    :return:
    """
    regex = '[vV]?[\d\.]+'
    result = re.findall(regex, source_str)
    if len(result) >= 1:
        return result[-1]
    else:
        return ''


def replace_many(source_str, replace_list, replace_str=''):
    """
    """
    p = re.compile('|'.join(replace_list))
    return p.sub(replace_str, source_str)


def extract_app_name(app_name):
    replace_list = ['安卓版', '手机版', '破解版', '修改版', '官方版', 'iOS版', 'IOS版']
    app_name = replace_many(app_name, replace_list)
    return app_name


def extract_size(source_str):
    regex = '[\d]+(?:\.[\d]+){0,1}[GgMmKk][Bb]?'
    result = re.findall(regex, source_str)
    if len(result) >= 1:
        return result[0]
    else:
        return ''


def chardet_detect(response):
    detector = UniversalDetector()
    for line in response.content.splitlines():
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result
