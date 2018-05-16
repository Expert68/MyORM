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

