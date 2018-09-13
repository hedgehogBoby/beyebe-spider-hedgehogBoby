
def dictToClazz(dictNow, clazz):
    lstKey = __props(clazz)
    # print(lstKey)
    # 组装语句
    strp = ''
    first = True
    # XiaociweiExtract(url=missionBean.url, type=missionBean.type)
    for name in lstKey:
        strNow = ','
        if first:
            strNow = ''
            first = False
        if type(dictNow.get(name)) == type({}):
            print("[warning]在处理时转换dict至str")
            strNow += "{}=str(dictNow.get('{}',None))".format(name, name)
        else:
            strNow += "{}=dictNow.get('{}',None)".format(name, name)
        strp += strNow
    strAll = 'zywa_database_core.model.xiaociweiModel.' + clazz.__name__ + "(" + strp + ")"
    print("[Info]执行转换语句:" + strAll)
    return eval(strAll)

def __props(obj):
    pr = []
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('_') and not callable(value) and name != 'metadata':
            pr.append(name)
    # 返回InstrumentedAttribute对象
    return pr


