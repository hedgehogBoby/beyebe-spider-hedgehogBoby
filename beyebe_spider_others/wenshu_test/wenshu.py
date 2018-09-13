import base64
import re

import execjs
import time

from beyebe_spider_others.wenshu_test.AES import decodeAESin67
from beyebe_spider_others.wenshu_test.wenshuUtilImp import wenshuUtilImp


class Wenshu(wenshuUtilImp):
    def __init__(self):
        jsstr = self._get_js('./js/Lawyee.CPWSW.ListExtend.js')
        self.ctx1 = execjs.compile(jsstr)  # 加载JS文件
        jsstr = self._get_js('./js/rawinflate.js')
        self.ctx2 = execjs.compile(jsstr)  # 加载JS文件

    def getKey(self, vjkl5):
        """
        function getKey() {
            var i = 25 - 10 - 8 - 2;
            var c = getCookie('vjkl5');
            var str = c.substr(i, i * 5) + c.substr((i + 1) * (i + 1), 3);
            var a = str.substr(i) + str.substr( - 4);
            var b = str.substr(4) + a.substr( - i - 1);
            c = hex_md5(str).substr(i - 1, 24);
            return c
        }
        :param vjkl5:
        :return:
        """
        key1 = self.ctx1.call('getKey', vjkl5)  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
        return key1

    def getDocID(self, selectDocId, runEval):
        """
        文档ID解密
        列表页,返回的list中,第一个元素中RunEval是个加密的字符串,然后看其他节点(文案列表)的"文书ID"也加密了
        然后两个关键方法:unzip()和com.str.Decrypt()
        列表页上执行com.str.Decrypt(unzip(文书ID))可以拿到docId明文
        然后你翻页发现不行了,那是因为RunEval这个值翻页后改变了,所以你在翻页后需要执行以下eval(unzip(RunEval))
        :param selectDocId:
        :param vjkl:
        :return:
        """
        sc2 = self._getUnzip(selectDocId)
        sc3 = decodeAESin67(sc2, self.get_KEY(runEval))
        return sc3

    def _getUnzip(self, b64Data):
        sc1 = base64.b64decode(b64Data)
        sc2 = self.ctx2.call('RawDeflate.inflate', str(sc1, 'utf-8'))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
        return sc2

    # 加载JS
    def _get_js(self, path):
        f = open(path, 'r', encoding='utf-8')  # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    def get_KEY(self, RunEval):
        """
        _KEY解密
        """
        js = self._getUnzip(RunEval)
        js_objs = js.split(";;")
        js1 = js_objs[0]
        js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
        jsstr = self._get_js('./js/test.js')
        jsstr = jsstr.replace("{js1}", js1).replace("{js2}", js2)
        ctxNow = execjs.compile(jsstr)
        msg = ctxNow.call('test')
        _KEY = re.search("\"(.*?)\"", msg, flags=0).group(1)

        return _KEY


if __name__ == '__main__':
    wenshu = Wenshu()
    wenshu.get_KEY(
        "w61Zw4tuwoMwEMO8FsKiHGwRw7UHUE7DucKEHlcWwqpIw5pwaMKIHHLCisOyw68FwppSHg7CmGDCiAkjwqFFw5jCu8OewpnDscOaYMKxw5zCh8Obw50pwpDDoTFewr/DhzI8fMK9fcOKw6h7wrPDv8KQwptowrtjwq7Do8KSwoDCscOawqwgAsOMPCrDpBXCiMOMZMK5YlfDgsOcw4JAdygLwoPDmcKDYsKYXMKwwoYmEAFyQBjDsAdhwqgDwp1ADsKUMAMwKATDuwzDtzx/wr0IwqLDgynClsOnIMKOw6TDgsOzw4kXw4nDhcKYe8K5wqZuw7l1wrlyw7rCjcKkw4QIw6EyJ8Orw6BUHjPDrWjDr8OJHsKXw78/wqbCicKlw43CiQc5aQ8JSm7ClcKEZXfDpxZwP1kFwrfDksK3EVNxNHV7wp4qQ13Cl8KoBkHDicKhYcOsHMKkwp7CosKFw4dWw5jCmh5dw5w6w7s+FsOQI8Kqb8KowpF4c8KDw5RLXVU0RcKfwr/ClTUADsOjwrTCjALCsxFdw5PDtmXCnsO8MMOTw406w644wpoFw53CusKhw54vdMOzwoAmWsOtw5PCr8OWURYEw5PDuAAwT0ddw4rDkyjDlmdwGwt9e8KyUcKRDF3DvMOTXcK4wq/ClsOCwqLCtMK3w5zDlTfCqcOWUcOJIm0Uw6fCoRolKn0VwqtbwosDUsKPE8Odw5MlwpsrCsOBGcO3fgA=")
    startTime=time.time()
    for i in range(100):
        vjkl = wenshu.getKey("f3d3fd16f9aff80c74801e6182e0315ce26bad92")
        print(vjkl)
        docId = wenshu.getDocID(
            "DcKNwrcRw4BADMKAVlIOwqXDksOvP8KSw51QccKQexAqwrxiwo7DjMOrw5zCiMKFBj/DmB/DtFrCvSDDtsKJYWHChDULw5nDncKUwqfDm0YFAcKrNCHDgxrDuxbDklA9awoswpsMw63CqHbDjj1Mwoxlw7Yaw7gUJ8OxGTQ8a8Kqw7bDisOkfw7ChMKrVcK0McKCw6J8w4bClcKRF8KPwpbDiR7Ct8KWwpTDh8O0w6lTwqLCmMOfwpVaw70zwqJ3w5nChnjDg8K5woknw7IB",
            "w61Zw5vCjsKCMBDDvRbCiA9tMMO+AMOxw4lPw5jDh0lDNsKoKw8rwqbDosKTw7HDnxcQWS5dw4DChWLCkcKTwpAxwrRzOXNmWsOawrg4BMObw53DmcKXw4EpWn9EMjh+wq3DtjLDvMOeHD7DpSbDnMOuwphjOSQgwowWS8KQADHCjw55wodEZsKyXMKxK8KhwrYQw6Adw4xCwqB6YAzDhQUTIAHCnCBhEAN2wpA1w7IHT0gOKcKhAhBoBMKjBHddb23Du8Ohw7Ecw4nCix/ChcOSdj3DskTDvDDDplxvwolaw75cb8Kcw67ClhQLIRxmwqUTwpzDij7Ck8KJw7bCmcO0dcOxw7vCnzTCsWQ4w5YgK8KZIUHDsU8lYFnDncOKDMO+DlbDgcKtw5Rtw4RUw7TCph7Dj0PCpcKow6sUw5UgKHNow7DCncKDw6zDhmjDocK1FXZHwo1nw5TCnsOWw73Cn0EPwqvCvsKmwoPDmA/Dp2RgTzrDnGnDs1ldGlNhwqLCsCkYXcOCHMOpYzM2wr91wodMw57CqCXDvsKCw7pobFTCvcK8wrTCksKjwps2fRvDkljCjE4KdsOTGcOQwoBmHcKLw4vDtmDCoyLDkRtxKmfClEnCncKlwowMwpvDhWbClXtNwqdbwptBw5wowq5mwrXClMKow7RZUsKPFh1Swo/Di8Olw4spwpsrCsOBGXd/AA==")
        print(docId)
    print(time.time()-startTime)


