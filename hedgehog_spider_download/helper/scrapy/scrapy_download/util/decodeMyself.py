import traceback

import chardet


def decodeMyself(response):
    try:
        html = response.body.decode()
    except:
        errMsg = traceback.format_exc()
        print("[decode]parse Warning,try charset:" + errMsg)
        try:
            html = response.body.decode(response.encoding)
        except:
            errMsg = traceback.format_exc()
            print("[decode]parse Warning,try charset:" + errMsg)
            charset = chardet.detect(response.body)['encoding']
            html = response.body.decode(charset)
    return html