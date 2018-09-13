from zywa_database_core.dao.mongo.mongoClientNew import db_spider


class MusicBean:
    def __init__(self):
        self.title = '讲真的'
        self.singers = ['曾惜']
        self.fromType = 2
        self.musicId = ''


if __name__ == '__main__':
    names = ['张三', '李四']
    names.sort()
    print(names)
    names = ['李四', '张三']
    names.sort()
    print(names)
    # db_spider['music_total'].save(MusicBean().__dict__)
