#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/20 9:58
# @Author  : lichangjian
import sys
import traceback


def _db_helper_result_config(objects=None, msg='', status=0):
    """
    数据库返回格式配置
    :param objects:
    :param msg:
    :param status:
    :return:
    """
    if isinstance(objects, list):
        count = len(objects)
    elif objects is None:
        count = 0
    elif isinstance(objects, dict):
        # 已按固定格式处理，直接返回
        if list(objects.keys()) == ['status', 'msg', 'count', 'objects']:
            return objects
        else:
            count = 1
    else:
        count = 1
    return {"status": status, "msg": msg, "count": count, "objects": objects}


def db_helper_result_format(func):
    """
    数据库返回格式规范化
    :param func:
    :return:
    """

    def to_convert_result(*args, **keyargs):
        try:
            return _db_helper_result_config(status=1, msg='success', objects=func(*args, **keyargs))
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            print('exc', exc_type, exc_instance, exc_traceback)
            print('traceback', traceback.format_exc())
            if len(exc_instance.args) >= 2:
                msg = exc_instance.args[0]
                objects = exc_instance.args[1]
            else:
                msg = str(exc_instance)
                objects = None
            return _db_helper_result_config(status=0, msg=msg, objects=objects)

    return to_convert_result
