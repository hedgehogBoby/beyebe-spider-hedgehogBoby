import os
import traceback

from selenium import webdriver

from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself
from zywa_database_core.dao.postgre.postgresqlHelper import PostgresqlHelper

fp = webdriver.FirefoxProfile()
pathDownload = os.getcwd() + '/test'
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", pathDownload)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(firefox_profile=fp, executable_path='/Users/magic/PycharmProjects/zywa-spider-xiaociwei/plug/geckodriver/mac/geckodriver')

items = PostgresqlHelper().select("""SELECT "public"."t_vague_mapping_apk_info".uuid,"public"."t_vague_mapping_apk_info"."apk_download_url" FROM "public"."t_vague_mapping_apk_info" WHERE "public"."t_vague_mapping_apk_info".status =2""")
driver.implicitly_wait(10)
driver.set_page_load_timeout(10)
driver.set_script_timeout(10)  # 这两种设置都进行才有效，未测试

pathOld = []
dictAns = {}
__mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")

for item in items:
    url = str(item[1])
    uuid = str(item[0])
    try:
        print('url= {} uuid={}'.format(url, uuid))
        driver.get(url)
    except:
        traceback.print_exc()
    # 阻塞直到没有.part文件
    while True:
        pathList = os.listdir(pathDownload)
        for path in pathList:
            if '.part' in path:
                continue
        break
    # 找到新增加的文件
    pathList = os.listdir(pathDownload)
    fileName = ''
    for path in pathList:
        if path in pathOld:
            continue
        else:
            fileName = path
            break
    pathOld = pathList
    if not fileName == '':
        dictNow = {'uuid': uuid, 'fileName': fileName}
        __mongoClient.saveDict(dictNow, tableName='test_file_webdriver_download')
