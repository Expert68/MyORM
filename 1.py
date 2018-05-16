import pymysql
from 池版 import settings
from DBUtils.PooledDB import PooledDB

pool = PooledDB(
    creator = pymysql,
    maxconnections=6,
    mincached=2,
    maxcached=5,
    maxshared=3,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host = settings.host,
    port = settings.port,
    user = settings.user,
    password = settings.password,
    database = settings.database,
    charset = settings.charset,
    autocommit = True
)

class Mysql:
    def __init__(self):
        self.conn = pool.connection()
        self.cursor = self.conn.cursor(cursor = pymysql.cursors.Dictcursor)

    def close_db(self):
        self.cursor.close()
        self.conn.close()


    def select(self,sql,args):
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

class Field:
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class StringField(Field):
    def __init__(self, name, column_type='varchar(32)', primary_key=False, default=None):
        super().__init__(name,column_type,primary_key,default)

class IntegerField(Field):
    def __init__(self, name, column_type='int', primary_key=False, default=0):
        super().__init__(name,column_type,primary_key,default)

class Modelsmeta(type):
    def __new__(cls, name,bases,attrs):
        if name == 'Model':
            return type.__new__(name,bases,attrs)
        table_name = attrs.get('table_name',None)
        if not table_name:
            table_name = name
        primary_key = None
        mapping = {}
        for k,v in attrs.items():
            if isinstance(v,Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        raise TypeError('主键重复')
                    primary_key = v

        for k in mapping:
            attrs.pop(k)

        attrs['table_name'] = table_name
        attrs['mapping'] = mapping
        attrs['primary_key'] = primary_key

class Model(dict,metaclass=Modelsmeta):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except Exception:
            raise TypeError('无该属性')

    @classmethod
    def select_one(cls1):
    ms = Mysql()








class User(Model):
    table_name = table_name
    id = IntegerField('id',primary_key=True)
    name = StringField('name')



