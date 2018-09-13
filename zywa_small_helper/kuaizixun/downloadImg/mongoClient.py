import pymongo


class CangMongoClient(object):
    def __init__(self, host="172.10.3.219",
                 port=20000, db="xiaociwei_alarm",
                 user="xiaociweialarmRWUser",
                 password="zywaXIAOCIWEI@!!!", ):
        self.MONGO_CONNECT_INFO = {
            "host": host,
            "port": port,
            "db": db,
            "user": user,
            "password": password,
        }

        self.new_client = pymongo.MongoClient(self.MONGO_CONNECT_INFO['host'], self.MONGO_CONNECT_INFO['port'])
        new_db = self.new_client[self.MONGO_CONNECT_INFO['db']]
        new_db.authenticate(self.MONGO_CONNECT_INFO["user"], self.MONGO_CONNECT_INFO["password"])

        self.new_db = new_db

    def close(self):
        self.new_client.close()
