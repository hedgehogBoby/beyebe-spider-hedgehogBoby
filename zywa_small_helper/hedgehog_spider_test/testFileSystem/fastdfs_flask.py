from flask import Flask,request
import flask
from fdfs_client.client import *
import logging
from flask.helpers import make_response

app = Flask(__name__)

tracker = get_tracker_conf(conf_path='client.conf')
client = Fdfs_client(tracker)
logger = logging.getLogger()
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

#测试
@app.route('/test.go', methods=["GET"])
def test():
    return '测试成功'


#上传
@app.route('/fastdfs', methods=["POST"])
def upload():
    if request.args.get("type") == "upload":
        try:
            dict_file = request.files['file'].__dict__
            print(dict_file)
            res_upload = client.upload_by_buffer(filebuffer=request.files['file'].read())
            logger.info(res_upload)
            return str(res_upload)
        except Exception as e:
            logger.info('上传文件失败: ', e)
            return '上传文件失败: ' +  e


#下载，删除
@app.route('/fastdfs', methods=["GET"])
def get():
#下载文件信息
    if request.args.get("type") == "download" and request.args.get("id")!=None and request.args.get("style")==None:
        try:
            res_download = client.download_to_buffer(remote_file_id=request.args.get("id"))
            logger.info(res_download)
            return str(res_download)
        except Exception as e:
            logger.info('下载文件失败，文件id无效或不存在: ' + str(e))
            return '下载文件失败，文件id无效或不存在: ' + str(e)

#下载文件  直接使用
    if request.args.get("type") == "download" and request.args.get("style") == "file" and request.args.get("id")!=None:
        try:
            res_download = client.download_to_buffer(remote_file_id=request.args.get("id"))
            response = make_response(res_download['Content'])
            response.headers['Download-Size'] = res_download['Download size']
            response.headers['Storage-IP'] = res_download['Storage IP']
            return response
        except Exception as e:
            logger.info('下载文件失败，文件id无效或不存在: ' + str(e))
            return '下载文件失败，文件id无效或不存在: ' + str(e)

#下载图片  直接使用
    if request.args.get("type") == "download" and request.args.get("style") == "image" and request.args.get("id")!=None:
        try:
            res_download = client.download_to_buffer(remote_file_id=request.args.get("id"))
            response = make_response(res_download['Content'])
            response.headers['Content-Type'] = 'image/png'
            response.headers['Download-Size'] = res_download['Download size']
            response.headers['Storage-IP'] = res_download['Storage IP']
            return response
        except Exception as e:
            logger.info('下载文件失败，文件id无效或不存在: ' + str(e))
            return '下载文件失败，文件id无效或不存在: ' + str(e)

#下载视频   直接使用
    if request.args.get("type") == "download" and request.args.get("style") == "video" and request.args.get("id")!=None:
        try:
            res_download = client.download_to_buffer(remote_file_id=request.args.get("id"))
            response = make_response(res_download['Content'])
            response.headers['Content-Type'] = 'video/mp4'
            response.headers['Download-Size'] = res_download['Download size']
            response.headers['Storage-IP'] = res_download['Storage IP']
            return response
        except Exception as e:
            logger.info('下载文件失败，文件id无效或不存在: ' + str(e))
            return '下载文件失败，文件id无效或不存在: ' + str(e)

#删除
    if request.args.get("type") == "delete" and request.args.get("id") != None:
        try:
            res_delete = client.delete_file(remote_file_id=request.args.get("id"))
            return str(res_delete)
        except Exception as e:
            logger.info('删除文件失败，文件id无效或不存在: ' + str(e))
            return '删除文件失败，文件id无效或不存在: ' + str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4540, threaded=True)

