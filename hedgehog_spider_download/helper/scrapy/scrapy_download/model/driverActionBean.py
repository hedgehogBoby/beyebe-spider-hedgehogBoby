class DriverActionBean:
    """
       NAME列表
       delay:延迟timeout时间
       waitfor:等待标签出现,该标签如果超时,不会影响下面的代码执行
       pushdown:下拉到最底部
       js:注入js
       """

    def __init__(self, name, msg, timeout=10):
        self.name = name
        self.msg = msg
        self.timeout = timeout


if __name__ == '__main__':
    action = DriverActionBean('test', 'test')
    print(action.timeout)