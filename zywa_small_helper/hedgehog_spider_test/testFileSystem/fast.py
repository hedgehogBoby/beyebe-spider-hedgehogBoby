from fdfs_client.client import *

print("start")
tracker = get_tracker_conf(conf_path='client.conf')
client = Fdfs_client(tracker)
print("upload")
res_upload = client.upload_by_file('/Users/magic/PycharmProjects/zywa-spider-xiaociwei/img/test.png')

print(res_upload)
print('end')
