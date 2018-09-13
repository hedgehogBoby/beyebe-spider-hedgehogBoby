class MiddlewareHttpGetImp():
    """
    继承该方法的中间件服务基于HTTP-GET提供给用户

    """

    def request(self, args, headers):
        return 'test success for get'

    def serverIPs(self):
        """
        部署集群IP及端口,返回字典数组
        :return:
        """
        return [{"ip": '192.168.0.1', 'port': '80'}]

    def version(self):
        """
        未完成完整异常处理的业务版本号不允许超过V1.0,为测试版
        :return:
        """
        return "V0.1"
