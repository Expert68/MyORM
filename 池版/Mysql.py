import pymysql
from 池版 import db_pool

class Mysql:
    def __init__(self):
        self.conn = db_pool.pool.connection()
        self.cursor = self.conn.cursor(
            cursor = pymysql.cursors.DictCursor
        )

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def select(self,sql,args=None):
        #select * from user where id=%s

        self.cursor.execute(sql,args)
        res = self.cursor.fetchall()
        return res


    def execute(self,sql,args):
        try:
            self.cursor.execute(sql,args)
            affected = self.cursor.rowcount
        except BaseException as e:
            print(e)
        else:
            return affected






