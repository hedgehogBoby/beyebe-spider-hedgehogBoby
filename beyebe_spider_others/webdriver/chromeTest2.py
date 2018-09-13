from bs4 import BeautifulSoup
from idna import unicode
from selenium import webdriver


# 企查查特有横竖表识别工具
def jsonFormat(tableTag):
    """
    递归调用,可以获得table所有json结果
    :return:
    """
    result = []
    # print(str(tableTag))
    print(tableTag.get('class', ['error']))
    if len(tableTag.get('class', ['error'])) > 1 or "序号" in str(tableTag):
        print("正常表")

        resultTitle = []
        # 标题行
        allcols = tableTag.select('th')
        for j, col in enumerate(allcols):
            resultTitle.append(col.text)

        allrows = tableTag.select('tr')
        for i, row in enumerate(allrows):
            if i == 0:
                # 如果标题行已经获取成功,就跳过。如果没有获取成功,就拿第一行当结果
                if len(resultTitle) > 0:
                    print("标题行:", resultTitle)
                    continue
                else:
                    allcols = tableTag.select('td')
                    for j, col in enumerate(allcols):
                        resultTitle.append(col.text)
                    print("标题行:", resultTitle)
            else:
                resultNow = {}
                allcols = row.select('td')
                for j, col in enumerate(allcols):
                    resultNow[resultTitle[j]] = col.text
                result.append(resultNow)

    else:
        resultDifferent = {}
        print("异形表")
        allrows = tableTag.select('td')
        valueNow = []
        keyNow = None
        for row in allrows:

            # print(row.get('class'))
            if row.get('class', ['error'])[0] == 'tb':
                # print("主")
                # 存储上一个表
                if keyNow is not None:
                    resultDifferent[keyNow] = valueNow
                keyNow = row.text
                valueNow = []
            else:
                # print("从")
                valueNow.append(row.text)
        result.append(resultDifferent)
    return result


driver = webdriver.Chrome(executable_path='/Users/magic/PycharmProjects/zywa-spider-xiaociwei/plug/chromedriver/mac/chromedriver')
driver.maximize_window()
driver.get('https://www.qichacha.com/creport_3f603703d59a04cbe427e5825099a565')
source = driver.page_source
bs4 = BeautifulSoup(source)
for i,tableTag in enumerate(bs4.select_one('div[class=\"panel-body tab-content\"]').select('table')):
    print("找到一个表格",i)
    print(tableTag)
    result = jsonFormat(tableTag)
    print(result)
driver.close()
