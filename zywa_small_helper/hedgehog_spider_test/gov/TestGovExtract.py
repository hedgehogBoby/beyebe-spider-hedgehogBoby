import re

from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself

if __name__ == '__main__':
    __mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")
    pattern = re.compile(r'>.{1,40}[g,n]ov.*?<')
    pattern2 = re.compile(r"http.?://.+?[/,$]")
    pattern3 = re.compile(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
    for item in __mongoClient.selectAll(tableName='baidu_gov'):
        print(item['seedTag'])
        html = item['html']
        resultList = pattern.findall(html)
        for result in resultList:
            try:
                # print(result)
                # 进行潜在的组装
                result2 = result[1:len(result) - 1]

                if not result2[1:4] == 'http':
                    result2 = 'http://' + result2

                # 抽取根目录
                result3 = pattern2.match(result2).group()
                # print(result3)
                # 最终检查一下是否是网址
                if pattern3.match(result3) is not None:
                    print('网址检测通过:' + result3)
                    dictSave = {}
                    dictSave['seedTag'] = item.get('seedTag')
                    dictSave['url'] = result3
                    __mongoClient.saveDict(dictSave, tableName='gov_portals')
                else:
                    print('网址检测失败:' + result3)
            except:
                continue
