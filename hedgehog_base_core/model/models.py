# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String, Text, Time, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Ippool(Base):
    __tablename__ = 'ippool'
    __table_args__ = (
        Index('ip+port', 'port', 'ip', unique=True),
    )

    id = Column(Integer, primary_key=True)
    updateTime = Column(DateTime)
    port = Column(Integer)
    msg = Column(String(255))
    ip = Column(String(16))
    createTime = Column(DateTime)
    cheak = Column(String(255))


class IppoolHistory(Base):
    __tablename__ = 'ippool_history'
    __table_args__ = (
        Index('ip+port', 'port', 'ip', unique=True),
    )

    id = Column(Integer, primary_key=True)
    updateTime = Column(DateTime)
    port = Column(Integer)
    msg = Column(String(255))
    ip = Column(String(16))
    createTime = Column(DateTime)
    cheak = Column(String(255))


class TAdministrativeDivision(Base):
    __tablename__ = 't_administrative_division'

    area_id = Column(Integer, primary_key=True)
    area_name = Column(String(32))
    area_name_abbr = Column(String(32))


class WechatAccount(Base):
    __tablename__ = 'wechat_account'

    id = Column(Integer, primary_key=True)
    type = Column(String(100, 'utf8mb4_bin'))
    account = Column(String(100, 'utf8mb4_bin'), nullable=False)
    spider_time = Column(Time)


class XiaociweiExtract(Base):
    __tablename__ = 'xiaociwei_extract'

    id = Column(Integer, primary_key=True)
    addTime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    url = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    title = Column(String(255), unique=True)
    info = Column(String(255))
    dbMsg = Column(String(255))
    missionCreateTime = Column(Integer)
    level = Column(Integer, nullable=False)
    errorNum = Column(Integer)
    errorNumMax = Column(Integer)
    timeout = Column(Integer)
    lstImgTag = Column(String(255))
    lstVideoTag = Column(String(255))
    lstIframeTag = Column(String(255))
    errMsg = Column(String(255))
    etc = Column(String(255))
    wordText = Column(Text)
    html = Column(Text)


class XunIppool(Base):
    __tablename__ = 'xun_ippool'
    __table_args__ = (
        Index('ip+port', 'port', 'ip', unique=True),
    )

    id = Column(Integer, primary_key=True)
    updateTime = Column(DateTime)
    port = Column(Integer)
    msg = Column(String(255))
    ip = Column(String(16))
    createTime = Column(DateTime)
    cheak = Column(String(255))
