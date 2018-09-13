class MiddlewareHttpGetImp():
    """
    TODO
    继承该方法的中间件服务基于REDIS提供给用户
    """
    def serverIPs(self):
        """
        部署集群IP,返回字典数组
        :return:
        """
        return [{"ip": '192.168.0.1'}]