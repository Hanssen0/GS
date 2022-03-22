import hashlib

from dt.DB_utils import POOL
import pymysql


def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cursor


def close_conn(conn, cursor):
    conn.close()
    cursor.close()


def select_all(sql, args):
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchall()
    print(result)
    close_conn(conn, cur)
    return result


def select_token(sql, args):
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchall()
    print('{} token: {}'.format(args, result))
    close_conn(conn, cur)
    return result


def token_insert(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("token insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


#查找记录是否存在

def select_record(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        if result==0:
            return True
        else:
            return False
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False




def record_insert(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("token insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


def user_insert(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("user insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


def select_user_login(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            username = r['userName']
            email = r['email']
            usertype = r['userType']
            print("select_user_login=>", username, email, usertype)
        if len(res) == 0:
            return ''
        return username, email, usertype
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_get_user(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True if result == 0 else False
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_get_user_info(args):
    conn, cur = create_conn()
    try:
        cur.execute("select * from user where userName = %s", args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            username = r['userName']
            email = r['email']
            usertype = r['userType']
            print("select_get_user_info=>", username, email, usertype)
        if len(res) == 0:
            return ''

        return {
            "username": username,
            "email": email,
            "usertype": usertype,
        }
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_get_userid(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        data = cur.fetchone()
        conn.commit()
        close_conn(conn, cur)
        return data['id']
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_records():
    conn, cur = create_conn()
    try:
        cur.execute("select * from record")
        result = cur.fetchall()
        conn.commit()
        close_conn(conn, cur)
        return result
    except Exception as e:
        print("records select except")
        conn.rollback()
        close_conn(conn, cur)
        return False


def encode_(str):
    MD5 = hashlib.md5()
    MD5.update(str.encode(encoding='utf-8'))
    print("加密后：", MD5.hexdigest())
    return MD5.hexdigest()


# sql = "select * from user where userName=%s "
# q = "🍺🐷"
# res = select_all(sql, q)
# print(res)
def update_token(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("user_token update except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def user_usertype_update(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        return True
    except Exception as e:
        print("user insert except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

def select_email(sql, args):
    conn, cur = create_conn()
    try:
        cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        res = cur.fetchall()
        for r in res:
            email = r['email']
        if len(res) == 0:
            return ''
        return email
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False


def update_pwd(sql, args):
    conn, cur = create_conn()
    try:
        result = cur.execute(sql, args)
        conn.commit()
        close_conn(conn, cur)
        if result == 1:
            return True
        return False
    except Exception as e:
        print("user select except", args)
        conn.rollback()
        close_conn(conn, cur)
        return False

