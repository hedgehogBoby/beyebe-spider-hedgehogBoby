# -*- coding: utf-8 -*-

"""
@version: ??
@author: djstava
@license: MIT Licence
@contact: djstava@gmail.com
@site: http://www.xugaoxiang.com/blog
@software: PyCharm
@file: SQLAlchemy.py
@time: 2017/3/22 10:42
"""

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义Channel对象:
class Channel(Base):
    # 表名
    __tablename__ = 'xiaociwei_extract'
    # 表结构
    id = Column(Integer(), primary_key=True)
    addtime = Column(Integer())
    url = Column(String(255))
    type = Column(Integer())
    title = Column(String(255))
    info = Column(String(255))
    dbMsg = Column(String(255))
    missionCreateTime = Column(Integer())
    level = Column(Integer())
    errorNum = Column(Integer())
    errorNumMax = Column(Integer())
    timeout = Column(Integer())
    lstImgTag = Column(String(255))
    lstVideoTag = Column(String(255))
    errMsg = Column(String(255))
    etc = Column(String(255))
    html = Column(String(65525))

    # id = Column(String(20), primary_key=True)
    # channel_name = Column(String(45))
    # address = Column(String(80))
    # service_name = Column(String(45))


def __init__(self, id, channel_name, address, service_name):
    self.id = id
    self.channel_name = channel_name
    self.address = address
    self.service_name = service_name


# 初始化数据库连接,:
engine = create_engine('mysql+pymysql://root:fn199544@bj-cdb-r4mhtei7.sql.tencentcdb.com:63814/news')
# 打开数据库连接
# db = pymysql.Connect(
#     host='bj-cdb-r4mhtei7.sql.tencentcdb.com',
#     port=63814,
#     user='root',
#     passwd='fn199544',
#     db='news',
#     charset='utf8'
# )
# 创建DBSession类型:
dBSession = sessionmaker(bind=engine)

session = dBSession()

# 增操作
item1 = Channel(url="testNew", type=1)
session.add(item1)

# item2 = Channel()
# session.add(item2)

# item3 = Channel(id='3', channel_name='catv3', address='http://10.10.10.188/catv3', service_name='economics')
# session.add(item3)

session.commit()
session.close()

# 查操作
session1 = dBSession()
channel = session1.query(Channel).filter(Channel.id < 3).all()

for i in range(len(channel)):
    print(channel[i].id)
    print(channel[i].url)
    print(channel[i].type)

session1.close()

# 改操作
# session2 = DBSession()
# session2.query(Channel).filter(Channel.id == '2').update({Channel.service_name: 'movie'}, synchronize_session=False)
# session2.commit()
# session2.close()

## 查看修改结果
# session3 = DBSession()
# print('\n')
# print(session3.query(Channel).filter(Channel.id == '2').one().service_name)
# session3.close()

# 删操作
# session4 = DBSession()
# session4.query(Channel).filter(Channel.id == '3').delete()
# session4.commit()
# session4.close()
