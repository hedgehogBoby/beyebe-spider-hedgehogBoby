import requests
import time
import json


### 上传文件 ###
url = 'http://172.10.3.43:4540/fastdfs?type=upload'
try:
    with open('upload.png','rb') as f:
        ### files的key一定要是file ###
        files = {'file':f.read()}
        response = requests.post(url, files=files)
    #返回的文件信息是str类型，需要转成字典    {'Group name': b'group1', 'Remote file_id': b'group1/M00/55/E4/rAoDIFrZo', 'Status': 'Upload successed.', 'Local file name': '', 'Uploaded size': '878B', 'Storage IP': b'172.10.3.32'}
    print(eval(response.text))
except:
    print(response.text)



### 下载文件 ###
# 第一种，返回该文件在文件系统里的信息 #
url = 'http://172.10.3.43:4540/fastdfs?type=download&id=group1/M00/5A/B4/rAoDIFraxb2AExqrAAADbtrz9fU9561183'
try:
    response = requests.get(url)
    #返回的文件信息是str类型，需要转成dict类型   {'Remote file_id': b'group1/M00/55/E4/rAoDIFrZon-AXWvWAAADbtrz9fU5496126', 'Content': b'\x89PNG\r\82', 'Download size': '878B', 'Storage IP': b'172.10.3.32'}
    response_dict = eval(response.text)
    print(response_dict)
    ##将文件数据存到本地
    with open('download11.png','wb') as f:
        f.write(response_dict['Content'])
except:
    print(response.text)

# 第二种，生成直接可以使用的网页，图片，视频等 ,该文件的信息在response的Headers里 #
url_file = 'http://172.10.3.43:4540/fastdfs?type=download&id=group2/M00/47/F2/rAoDIVravZqAKjx6AABlHWuAUKc0055722&style=file'
url_image = 'http://172.10.3.43:4540/fastdfs?type=download&id=group2/M00/47/E7/rAoDIVraur-AGegLAC7FHJY159E1594581&style=image'
url_video = 'http://172.10.3.43:4540/fastdfs?type=download&id=group2/M00/47/E1/rAoDIVrauRCAOL0HACdOQ7dHUQU6663095&style=video'

### 删除文件 ###
url = 'http://172.10.3.43:4540/fastdfs?type=delete&id=group1/M00/5A/B4/rAoDIFraxb2AExqrAAADbtrz9fU9561183'
try:
    response = requests.get(url)
    #返回的文件信息的是str类型，需要转成tuple     ('Delete file successed.', b'group1/M00/4D/F8/rAoDIFrWp0uAAbz7AAAAAAAAAAA082.txt', b'172.10.3.32')
    print(eval(response.text))
except:
    print(response.text)


