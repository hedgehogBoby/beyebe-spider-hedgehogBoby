# -*- coding: utf-8 -*-
import json

from sqlalchemy import Column, String, create_engine, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from zywa_database_core.model.xiaociweiModel import WechatAccount, TAdministrativeDivision, XiaociweiExtract


# 自动生成models:pip install sqlacodegen
# cd /Users/magic/PycharmProjects/zywa_crawl_platform/zywa_database_core/model
# sqlacodegen mysql://root:mypass@172.10.3.104:3306/xiaociwei?charset=utf8 > xiaociweiModel.py
# sqlacodegen mysql://root:mypass@172.10.3.104:3306/xiaociwei?charset=utf8 > /Users/magic/PycharmProjects/zywa_crawl_platform/zywa_database_core/model/xiaociweiModel.py

# 如果是Python3 还需要进入sqlacodegen的__init__内 增加一段语句
# import pymysql
# pymysql.install_as_MySQLdb()
# 就可以执行了
class MysqlClient:

    def __init__(self, connectUrl):
        self.connectUrl = connectUrl
        self.Base = declarative_base()
        # 'mysql+pymysql://root:mypass@172.10.3.104:3306/xiaociwei?charset=utf8'
        self.mysqlInit(connectUrl)

    def mysqlInit(self, connectUrl):
        # 初始化数据库连接,:
        self.engine = create_engine(connectUrl, encoding='utf-8', convert_unicode=True)
        # 创建DBSession类型:
        self.dBSession = sessionmaker(bind=self.engine)
        session = self.dBSession()
        try:
            session.execute('SET NAMES utf8;')
            session.execute('SET CHARACTER SET utf8;')
            session.execute('SET character_set_connection=utf8;')
        finally:
            session.close()

    def selectAll(self, clazz):
        # 根据tableName找到表名对应的class
        session = self.dBSession()
        try:
            lstAll = session.query(clazz).all()
            return lstAll
        finally:
            session.close()

    def removeAllAndInsertAll(self, lstItem, clazz):
        session = self.dBSession()
        try:
            # session.execute('DELETE FROM ')
            session.query(clazz).filter().delete(synchronize_session=False)
            session.add_all(lstItem)
            session.commit()
        finally:
            session.close()

    def removeOne(self, item):
        pass

    def insert(self, item):
        session = self.dBSession()
        try:
            session.add(item)
            session.commit()
        finally:
            session.close()

    def insertXiaociweiExtract(self, missionBean):
        session = self.dBSession()
        try:
            item1 = XiaociweiExtract(
                url=missionBean.url,
                type=missionBean.type,
                title=missionBean.title.strip(),  # title去除无效字符
                info=json.dumps(missionBean.info),
                dbMsg=missionBean.dbMsg,
                missionCreateTime=missionBean.missionCreateTime,
                level=missionBean.level,
                errorNum=missionBean.errorNum,
                errorNumMax=missionBean.errorNumMax,
                timeout=missionBean.timeout,
                lstImgTag=json.dumps(missionBean.lstImgTag),
                lstVideoTag=json.dumps(missionBean.lstVideoTag),
                lstIframeTag=json.dumps(missionBean.lstIframeTag),
                errMsg=missionBean.errMsg,
                etc=missionBean.etc,
                wordText=missionBean.wordText,
                html=missionBean.html
            )
            session.add(item1)
            session.commit()
        finally:
            session.close()

    def selectDivsion(self):

        session1 = self.dBSession()
        try:
            # 查操作
            # channel = session1.query(WechatAccount).filter(WechatAccount.id < 3).all()
            lstDivsion = session1.query(TAdministrativeDivision).all()
            return lstDivsion
        finally:
            session1.close()

    def selectWechatAccount(self):

        session1 = self.dBSession()
        try:
            # 查操作
            # channel = session1.query(WechatAccount).filter(WechatAccount.id < 3).all()
            lstWechatAccount = session1.query(WechatAccount).all()
            return lstWechatAccount
        finally:
            session1.close()
