import pymysql
from dbutils.pooled_db import PooledDB
from init_utils import *
password = init_by_key('SQL_PSD').strip()
root = init_by_key('root')


h = '127.0.0.1'
if(root=='/Users/oo/STUDY/STUDY/Postgraduate/papers/GS/' or root =='/var/www/GS/'):
    h ='43.129.28.10'

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
    host=h,
    port=3306,
    user='root',
    password=password,
    database='grading_system',
    charset='utf8mb4'
)

