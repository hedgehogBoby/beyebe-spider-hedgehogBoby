import datetime

import pytz
from bson import ObjectId

# _id = ObjectId("666f6f2d6261722d71757578")
# date = _id.generation_time
# # 修改时区
# date = date.astimezone(pytz.timezone('Asia/Shanghai'))
# print(date)
"""
查最近十分钟的入库情况
"""
# client = getMongoCircleClient()
dateNow = datetime.datetime.now() - datetime.timedelta(days=8, hours=0, minutes=0, seconds=0)
dateNow = dateNow.astimezone(pytz.timezone('utc'))
dummy_id = ObjectId.from_datetime(dateNow)
print(dummy_id)
# result = client.find({"_id": {"$gte": dummy_id}}, tableName='circle_recrawling_info')
# print(str(result.count()))
