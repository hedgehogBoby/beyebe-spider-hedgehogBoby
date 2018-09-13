#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/21 8:55
# @Author  : lichangjian
import pandas as pd
from sqlalchemy import create_engine
import sys

from zywa_database_core.dao.postgre.db import BaseTable
from zywa_database_core.dao.postgre.util.result_util import db_helper_result_format
from zywa_database_core.dao.postgre.util.string_util import parse_db_connect_url


class RelationalDatabaseHelper(object):
    def __init__(self, connect_url=''):
        """
        加载数据库
        """
        connect_info = parse_db_connect_url(connect_url)
        self.connect_info = connect_info
        self.__table_helper = None

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __getitem__(self, name):
        """
        指定待操作数据库,生成数据库对象
        :param name:
        :return:
        """
        self.__table_helper = TableHelper(self.connect_info, name)
        return self.__table_helper

    def get_table(self, name):
        return self.__getitem__(name)


class TableHelper(BaseTable):
    """
    数据库表格操作对象，封装对数据库表格操作
    """

    def __init__(self, connect_info, table_name):
        super(TableHelper, self).__init__()

        self._engine = create_engine(
            '{dbtype}://{name}:{pwd}@{host}:{port}/{database}'.format(dbtype=connect_info['dbtype'],
                                                                      name=connect_info['username'],
                                                                      pwd=connect_info['password'],
                                                                      host=connect_info['host'],
                                                                      port=connect_info['port'],
                                                                      database=connect_info['database']),
            pool_size=100, pool_recycle=3600)

        self.__table = table_name

        if not self.__table:
            raise Exception('请指定待操作数据库')

    def __find(self, db_sql):
        """
        数据库查询
        :param db_sql: 待执行sql
        :return:
        """
        result_df = pd.read_sql_query(db_sql, self._engine)
        result_df = result_df.fillna('')  # 处理数据中空值
        result = result_df.to_dict('records')
        # key = result_df.columns
        #
        # result_np = np.array(result_df)
        # result_list = result_np.tolist()
        #
        # result = [dict(zip(key, result_item)) for result_item in result_list]
        return result

    def __insert(self, documents, callback):
        """
        数据库插入，表不存在，自动创建
        :param documents:待插入列表
        :return:
        """
        df = pd.DataFrame(documents)
        try:
            df.to_sql(self.__table, self._engine, if_exists='append', index=False)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            raise Exception(str(exc_instance), callback)
        if callback:
            return callback
        return True

    @db_helper_result_format
    def find_one(self, filters):
        assert isinstance(filters, dict)
        sql = TableHelper.generate_sql(self.__table, filters, 1)
        return self.__find(sql)

    @db_helper_result_format
    def find_many(self, filters):
        assert isinstance(filters, dict)
        sql = TableHelper.generate_sql(self.__table, filters)
        return self.__find(sql)

    @db_helper_result_format
    def insert_one(self, document, callback=None):
        """
        单条插入
        :param document: 待插入字典
        :return:
        """
        assert isinstance(document, dict)
        return self.__insert([document], callback)

    @db_helper_result_format
    def insert_many(self, documents, callback=None):
        """
        批量插入
        :param documents:待插入字典
        :return:
        """
        assert isinstance(documents, list)
        return self.__insert(documents, callback)

    @staticmethod
    def generate_sql(name, fileters, limit=None):
        where_params = []
        assert isinstance(fileters, (dict, str))

        if isinstance(fileters, str):
            return str

        for param in fileters.keys():
            value = fileters[param]
            if isinstance(value, str):
                # where_sql += "and '%s' " % value
                where_params.append(" %s = '%s' " % (param, value))
            elif isinstance(value, (int, float)):
                where_params.append(" %s = %d " % (param, value))
            elif isinstance(value, bool):
                where_params.append(" %s = %s " % (param, str(value)))
        where_sql = 'where ' + 'and'.join(where_params)
        _sql = 'select * from {table} {where_sql}'.format(table=name, where_sql=where_sql)

        if limit and isinstance(limit, int):
            _sql = '{sql} limit {num}'.format(sql=_sql, num=limit)
        print(_sql)
        return _sql

    def get_conn(self):
        return self._engine.connect()

    @staticmethod
    def get_trans(conn):
        from sqlalchemy.engine.base import Connectable
        assert isinstance(conn, Connectable)
        return conn.begin()

    @staticmethod
    def rollback_tran(trans):
        from sqlalchemy.engine.base import RootTransaction
        assert isinstance(trans, RootTransaction)
        return trans.rollback()

    @staticmethod
    def commit_tran(trans):
        from sqlalchemy.engine.base import RootTransaction
        assert isinstance(trans, RootTransaction)
        return trans.commit()
