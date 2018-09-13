class MiddlewareHttpPostImp():
    """
    继承该方法的中间件服务基于HTTP-GET提供给用户
    """

    def request(self, args, postMsg, headers):
        return 'test success for post'

    def serverIPs(self):
        """
        部署集群IP及端口,返回字典数组
        :return:
        """
        return [{"ip": '192.168.0.1', 'port': '80'}]
