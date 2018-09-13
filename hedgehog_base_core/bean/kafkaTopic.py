# V0.2 TOPIC信息
# 2018/7/14
TOPIC_NEWS_PUBLISH = 'topic.circle.content.publish'  # 新闻发布topic
TOPIC_VIDEO_PUBLISH = 'topic.circle.video.publish'  # video发布topic
TOPIC_NEWS_PENDING = 'topic.circle.content.pending'  # 过滤后回调新闻topic
TOPIC_VIDEO_PENDING = 'topic.circle.video.pending'  # 过滤后回调视频topic

GROUP_NAME_MOVIE_PUBLISH = 'movies_data_group'  # 彭志豪影视中心消费groupName
GROUP_NAME_CIRCLE_FILTER = 'circle_topic_group'  # 杨克南过滤接口消费groupName
# GROUP_NAME_NEWS_PUBLISH='news_publish_group' #方楠 发布新闻接口消费groupName
GROUP_NAME_GIRLS_PUBLISH = 'girls_publish_group'  # 方楠 发布美女新闻接口消费groupName
# kafka Host 添加如下配置
# Linux位置: /etc/hosts
# MAC位置: /private/etc/hosts
# Windows: c:\windows\system32\drivers\etc
"""
172.10.4.4 Master.Hadoop
172.10.4.5 Slave1.Hadoop
172.10.4.6 Slave2.Hadoop
172.10.4.4 master.hadoop
172.10.4.5 slave1.hadoop
172.10.4.6 slave2.hadoop
"""
