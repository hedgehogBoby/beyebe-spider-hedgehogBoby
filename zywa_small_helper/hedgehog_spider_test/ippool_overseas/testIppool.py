import requests

if __name__ == '__main__':
    proxies = {"http": "http://198.15.135.26:8090", "https": "https://198.15.135.26:8090", }
    print(requests.get("http://www.baidu.com", proxies=proxies).text)
