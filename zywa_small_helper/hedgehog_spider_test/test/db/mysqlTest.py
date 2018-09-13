import pymysql


def mysqlInit():
    global db
    # 打开数据库连接
    db = pymysql.Connect(
        host='bj-cdb-r4mhtei7.sql.tencentcdb.com',
        port=63814,
        user='root',
        passwd='fn199544',
        db='news',
        charset='utf8'
    )

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)


def closeDb():
    # 关闭数据库连接
    db.close()


def insert(missionBean):
    cur = db.cursor()
    print("insert missionBean")
    sql_insert = """insert into xiaociwei_extract(url,type) values('哈哈',0)"""
    try:
        cur.execute(sql_insert)
        # 提交
        db.commit()
    except Exception as e:
        print(str(e))
        # 错误回滚
        db.rollback()


mysqlInit()
insert(None)
closeDb()
