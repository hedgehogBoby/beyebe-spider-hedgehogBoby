import requests



html = requests.get('http://www.bjcc.gov.cn/').text()
print(html)

if '3390E28916150173E053012819ACB99E' in html:
    print("yes")
