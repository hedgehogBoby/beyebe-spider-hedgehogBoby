import json

from zywa_database_core.dao.mongo.mongoClientMyself import getMongoDownloadClient
from scrapy.http import Request
from scrapy.spiders import Spider

from zywa_extract_helper.model.missionBean import MissionBean
from zywa_ippool_util.helper.iPPoolHelper import getRandomOneIP


class Rank(Spider):
    # mongodb
    client = getMongoDownloadClient()
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)
    name = 'rank'
    start_url = 'https://is.snssdk.com/api/news/feed/v81/?list_count=0&category=news_hot&refer=1&refresh_reason=5&session_refresh_idx=1&count=20&last_refresh_sub_entrance_interval=1528516626&loc_mode=7&loc_time=1528516579&latitude=22.495179&longitude=113.910721&city=%E6%B7%B1%E5%9C%B3%E5%B8%82&tt_from=enter_auto&lac=9519&cid=111856899&plugin_enable=3&iid=30029603170&device_id=48527931773&ac=wifi&channel=smartisan&aid=13&app_name=news_article&version_code=666&version_name=6.6.6&device_platform=android&ab_version=124645%2C293033%2C361029%2C374078%2C271178%2C357705%2C326524%2C326532%2C295827%2C353305%2C346607%2C373045%2C369463%2C239097%2C170988%2C371590%2C368831%2C374095%2C341396%2C374118%2C374230%2C368303%2C367787%2C330630%2C297058%2C374249%2C276205%2C286212%2C350193%2C365037%2C373740%2C367078%2C372146%2C277718%2C342055%2C372346%2C364453%2C366060%2C369501%2C369165%2C368839%2C373120%2C371553%2C371957%2C374139%2C372903%2C366037%2C366832%2C323233%2C341724%2C371778%2C363824%2C346556%2C341305%2C372620%2C345191%2C362185%2C214069%2C31210%2C338062%2C333969%2C366870%2C373693%2C280448%2C281293%2C366491%2C325611%2C324095%2C373886%2C369268%2C374010%2C373770%2C357401%2C365937%2C288417%2C290195%2C361350%2C370017%2C353483%2C252784%2C323964&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=100168%2C94570%2C102750%2C181430&ab_feature=94570%2C102750&abflag=3&ssmix=a&device_type=OS105&device_brand=SMARTISAN&language=zh&os_api=25&os_version=7.1.1&uuid=867955030391269&openudid=78865d99af75004e&manifest_version_code=666&resolution=1080*2070&dpi=400&update_version_code=66611&_rticket=1528516626743&plugin=10607&fp=PSTqJzGWFMKuFlG1L2U1FYweLlKS&pos=5r_-9Onkv6e_eyoseAEueCUfv7G_8fLz-vTp6Pn4v6esrK6zpKytqq-ssb_x_On06ej5-L-nr6-zqaSorKqksb_88Pzt3vTp5L-nv3sqLHgBLnglH7-xv_zw_O3R8vP69Ono-fi_p6ysrrOkrKuqpKyxv_zw_O3R_On06ej5-L-nr6-zqaSvqq6k4A%3D%3D&rom_version=25&ts=1528516626&as=a2456511f221bbd0ab0553&mas=007593a97e7064c523f9c3f966e71ac03a664e2660646e0ea2&cp=57b118b55f012q1'
    start_urls = []
    for i in range(32):
        start_urls.append(start_url)

    isFirst = True
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.1; OS105 Build/NMF26X) NewsArticle/6.6.2 okhttp/3.7.0.6'}

    def parse(self, response):
        try:
            jsonObj = json.loads(response.text)
            print('抓取新闻数目', len(jsonObj['data']))
            for data in jsonObj['data']:
                jsonNowObj = json.loads(data['content'])
                print(jsonNowObj['title'])
                missionBean = MissionBean(response.url, 0, ['train_rank'])
                missionBean.title = jsonNowObj['title']
                missionBean.info = jsonNowObj
                missionBean.info.update({'news_type': '头条热点流', 'resource': '头条推荐流'})
                if missionBean.info.get('tag') == 'ad':
                    print('这是个广告,过滤')
                    continue

                self.client.save(missionBean)
        finally:
            ipDict = getRandomOneIP()
            yield Request(url=response.url, headers=self.headers, dont_filter=True, meta={'proxy': 'http://' + ipDict['ip'] + ':' + ipDict['port']})

    def start_requests(self):

        for url in self.start_urls:
            ipDict = getRandomOneIP()
            ipMeta = {'proxy': 'http://' + ipDict['ip'] + ':' + ipDict['port']}
            yield Request(url, callback=self.parse, headers=self.headers, meta=ipMeta, dont_filter=True)
