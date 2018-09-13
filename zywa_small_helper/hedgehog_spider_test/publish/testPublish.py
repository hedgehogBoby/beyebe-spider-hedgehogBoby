import json

import requests

if __name__ == '__main__':
    url = 'http://circle.api.idianyou.cn/circle_api/circle/transpondRobotDynamicForAutoPublish.do'

    response = requests.post(url)
    f = open("test.json", encoding='utf-8')
    info = json.load(f)

    dataTest2 = {'content': json.dumps([info])}

    response = requests.post(url, data=dataTest2)

    print(response.text)
