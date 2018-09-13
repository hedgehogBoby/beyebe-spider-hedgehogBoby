import psycopg2


class PostgresqlHelper(object):

    def __init__(self):
        self.conn = psycopg2.connect(database="db_app", user="postgres", password="123456", host="172.10.3.170", port="5432")
        self.cur = self.conn.cursor()

    def insert(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def select(self, sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.close()
        return res
