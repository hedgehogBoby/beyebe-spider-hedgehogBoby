"""
文书工具类调用接口
2018/9/11 V0.1
p.s.预计本周出 V0.2 完全脱离JS版工具类
by fangnan
"""


class wenshuUtilImp:
    def getKey(self, vjkl5):
        """
        使用cookie中的vjkl5,获取实际的vjkl,从而可以发起POST请求

        :param wenshu.court.gov.cn/cookie/vjkl5
        :return:
        """
        pass

    def getDocID(self, selectDocId, runEval):
        """
        通过接口中的加密文档ID+runEval,获得真正的DocID

        :param
        selectDocId:文档ID
        runEval:runEval
        :return:
        """
        pass
