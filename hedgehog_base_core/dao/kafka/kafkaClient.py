import json

from pykafka import KafkaClient

from zywa_database_core.bean.kafkaTopic import TOPIC_NEWS_PUBLISH, TOPIC_VIDEO_PUBLISH, TOPIC_NEWS_PENDING, TOPIC_VIDEO_PENDING, GROUP_NAME_GIRLS_PUBLISH
from zywa_database_core.bean.newsBeanKafka import getTestNewsBean, getTestVideoBean

client = KafkaClient(hosts="172.10.33.105:9092")

newsProducer = None
videoProducer = None
newsConsumer = None
videoConsumer = None
girlsConsumer = None


def producerNews(newsBean, **kwargs):
    global newsProducer
    if newsProducer is None:
        newsProducer = client.topics[bytes(TOPIC_NEWS_PUBLISH, encoding='utf-8')].get_producer()

    kafkaDict = {'fromType': newsBean.fromType,
                 'isFilter': kwargs.get('isFilter', 1),
                 'data': newsBean.__dict__
                 }
    jsonStr = json.dumps(kafkaDict, ensure_ascii=False)
    return newsProducer.produce(bytes(jsonStr, encoding='utf-8'))


def producerVideo(newsBean, **kwargs):
    global videoProducer
    if videoProducer is None:
        videoProducer = client.topics[bytes(TOPIC_VIDEO_PUBLISH, encoding='utf-8')].get_producer()

    kafkaDict = {'fromType': newsBean.fromType,
                 'isFilter': kwargs.get('isFilter', 1),
                 'data': newsBean.__dict__}
    jsonStr = json.dumps(kafkaDict, ensure_ascii=False)
    return videoProducer.produce(bytes(jsonStr, encoding='utf-8'))


# TODO 按道理来讲,都因该在PENDING中消费,克南未做过滤之前,都使用PUBLSIH消费

def getPendingNewsConsumer():
    global newsConsumer
    if newsConsumer is None:
        newsConsumer = client.topics[bytes(TOPIC_NEWS_PENDING, encoding='utf-8')].get_simple_consumer(consumer_group=b'release_new', auto_commit_enable=True, auto_commit_interval_ms=1)
    return newsConsumer


def getPendingVideoConsumer():
    global videoConsumer
    if videoConsumer is None:
        videoConsumer = client.topics[bytes(TOPIC_VIDEO_PENDING, encoding='utf-8')].get_simple_consumer(consumer_group=b'release_new', auto_commit_enable=True, auto_commit_interval_ms=1)
    return videoConsumer


def getPendingGirlConsumer():
    global girlsConsumer
    if girlsConsumer is None:
        girlsConsumer = client.topics[bytes(TOPIC_NEWS_PUBLISH, encoding='utf-8')].get_simple_consumer(consumer_group=bytes(GROUP_NAME_GIRLS_PUBLISH, encoding='utf-8'), auto_commit_enable=True, auto_commit_interval_ms=1)
    return girlsConsumer


if __name__ == '__main__':
    for i in range(10000):
        newsBean = getTestNewsBean()
        msg = producerNews(newsBean)
        videoBean = getTestVideoBean()
        msg2 = producerVideo(videoBean)
    consumerTest1 = client.topics[bytes(TOPIC_NEWS_PUBLISH, encoding='utf-8')].get_simple_consumer(consumer_group=b'release_test', auto_commit_enable=True, auto_commit_interval_ms=1)
    consumerTest2 = client.topics[bytes(TOPIC_VIDEO_PUBLISH, encoding='utf-8')].get_simple_consumer(consumer_group=b'release_test', auto_commit_enable=True, auto_commit_interval_ms=1)
    for ans1 in consumerTest1:
        print("消费一条news结果")
        print(ans1.value.decode())
        break

    for ans2 in consumerTest2:
        print("消费一条video结果")
        print(ans2.value.decode())
        break
