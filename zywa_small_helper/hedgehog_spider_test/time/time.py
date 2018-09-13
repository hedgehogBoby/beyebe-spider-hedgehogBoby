import datetime
import time

# 获取当前时间, 其中中包含了year, month, hour, 需要import datetime
today = datetime.date.today()
print(today)
print(today.year)
print(today.month)
print(today.day)
'''
>>>2017-01-01
>>>2017
>>>1
>>>1
'''

# 获得明天, 其他依次类推
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
print(tomorrow)
'''
>>>2017-01-02
'''

# 获得昨天, 其他依次类推
today = datetime.date.today()
yestoday = today + datetime.timedelta(days=-1)
print(yestoday)

# 时间相减，相加同理
now = datetime.timedelta(days=0, hours=0, minutes=3, seconds=50);
pre = datetime.timedelta(days=0, hours=0, minutes=1, seconds=10);

duration_sec = (now - pre).seconds
duration_day = (now - pre).days
print(type(duration_sec))
print(type(now - pre))
print(duration_sec)
print(duration_day)
'''
>>><class 'int'>
>>><class 'datetime.timedelta'>
>>>160
>>>0
'''

# 使用time.strftime(format, p_tuple)获取当前时间，需要import time
print('使用time.strftime(format, p_tuple)获取当前时间，需要import time')
now = time.strftime("%H:%M:%S")

print(now)
'''
>>>23:49:34
'''
print("使用datetime.now()")
# 使用datetime.now()
now = datetime.datetime.now()
print(now)
print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)
print(now.microsecond)
print(now.strftime('%Y%m%d'))
'''
>>>2017-01-01 23:49:34.789292
>>>2017
>>>1
>>>1
>>>23
>>>49
>>>34
>>>789292
'''

# time和datatime的转换
print("time和datatime的转换")
datatimeNow = datetime.date.fromtimestamp(time.time())
timeNow = time.gmtime(datetime.datetime.now().timestamp())
print(datatimeNow)
print(timeNow)
