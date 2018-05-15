import settings

import pymysql

class mysql:
    __instance = None

    def __init__(self):
        self.conn = pymysql.connect(
            host = settings.host,
            port = settings.port,
            user = settings.user,
            password = settings.password,
            database = settings.database,
            charset = settings.charset,
        )
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        self.cursor.close()



    def select(self,sql,args=None):
        self.cursor.execute(sql,args)
        res = self.cursor.fetchall()
        return res

    def execute(self,sql,args=None):
        self.cursor.execute(sql,args)
        affected_row = self.cursor.rowcount
        return affected_row

    @classmethod
    def singleton(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance







