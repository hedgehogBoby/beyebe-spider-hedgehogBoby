# from splinter.driver.webdriver.chrome import Options, Chrome
# from splinter.browser import Browser
from contextlib import closing
import requests, json, time, re, os, sys, time
from bs4 import BeautifulSoup


def get_video_urls(user_id):
    video_names = []
    video_urls = []
    unique_id = ''
    while unique_id != user_id:
        # test_url='https://api.amemv.com/aweme/v1/discover/search/?cursor=0&keyword=6796248446&count=10&type=1&retry_type=no_retry&iid=17900846586&device_id=34692364855&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme&version_code=162&version_name=1.6.2&device_platform=android&ssmix=a&device_type=MI+5&device_brand=Xiaomi&os_api=24&os_version=7.0&uuid=861945034132187&openudid=dc451556fc0eeadb&manifest_version_code=162&resolution=1080*1920&dpi=480&update_version_code=1622'
        search_url = 'https://api.amemv.com/aweme/v1/discover/search/?cursor=0&keyword=%s&count=10&type=1&retry_type=no_retry&iid=17900846586&device_id=34692364855&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme&version_code=162&version_name=1.6.2&device_platform=android&ssmix=a&device_type=MI+5&device_brand=Xiaomi&os_api=24&os_version=7.0&uuid=861945034132187&openudid=dc451556fc0eeadb&manifest_version_code=162&resolution=1080*1920&dpi=480&update_version_code=1622' % user_id
        req = requests.get(url=search_url, verify=False)
        html = json.loads(req.text)
    aweme_count = html['user_list'][0]['user_info']['aweme_count']
    uid = html['user_list'][0]['user_info']['uid']
    nickname = html['user_list'][0]['user_info']['nickname']
    unique_id = html['user_list'][0]['user_info']['unique_id']
    user_url = 'https://www.douyin.com/aweme/v1/aweme/post/?user_id=%s&max_cursor=0&count=%s' % (uid, aweme_count)
    req = requests.get(url=user_url, verify=False)
    html = json.loads(req.text)
    i = 1
    for each in html['aweme_list']:
        share_desc = each['share_info']['share_desc']
        if '抖音-原创音乐短视频社区' == share_desc:
            video_names.append(str(i) + '.mp4')
            i = 1
        else:
            video_names.append(share_desc + '.mp4')
            video_urls.append(each['share_info']['share_url'])

        return video_names, video_urls, nickname


if __name__ == '__main__':
    print(get_video_urls('6796248446'))
