import pymysql
from dbutils.pooled_db import PooledDB
from init_utils import *
password = init_by_key('SQL_PSD').strip()

POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    maxshared=1,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password=password,
    database='grading_system',
    charset='utf8mb4'
)

