from sqlalchemy import create_engine
from sqlalchemy.sql import text
import hashlib
import pymysql
import pandas as pd
import os


def post_in_sql_dev_status(request):
    obs_code = str(request['obs']).upper()
    date0 = int(request['date0'])  # unix time sec
    dev_code = str(request['dev']).upper()
    date1 = int(request['date1'])  # unix time ms
    filename = str(request['filename']).lower()
    md5_hash = hashlib.md5(str(request['md5']).encode('utf-8')).digest()  # 16 byte binary file hash

    try:
        conn = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                               user=os.getenv('SQL_USER'),
                               passwd=os.getenv('SQL_PSW'),
                               db=os.getenv('SQL_DB'),
                               charset='utf8mb4', )
        cur = conn.cursor()
        sql = """INSERT INTO %s VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(sql, (os.getenv('SQL_TABLE'), obs_code, date0, dev_code, date1, filename, md5_hash))
        conn.commit()
        conn.close()
        return 1
    except Exception as E:
        print(E)
        return 0


def get_from_sql_dev_status(request):
    obs_code = str(request['obs']).upper()
    date0_from = int(request['date0_from'])
    date0_to = int(request['date0_to'])
    date1_from = int(request['date1_from'])
    date1_to = int(request['date1_to'])
    filename = str(request['filename']).lower()
    dev_code = str(request['dev']).upper()

    try:
        #   подключение к sql таблице на сервере imagdb.gcras.ru
        db = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                             user=os.getenv('SQL_USER'),
                             passwd=os.getenv('SQL_PSW'),
                             db=os.getenv('SQL_DB'),
                             charset='utf8mb4', )

        request = "SELECT * FROM %s WHERE obs='%s' AND dev='%s' AND filename='%s' AND" \
                  "date0 BETWEEN %s AND %s AND date1 BETWEEN %s AND %s" % (
                      os.getenv('SQL_TABLE'), obs_code, dev_code, filename,
                      date0_from, date0_to, date1_from, date1_to)
        cur = db.cursor()
        cur.execute(request)
        respond = cur.fetchall()
        db.close()
        df = pd.DataFrame(respond)
        return {}
    except Exception as E:
        print(E)
        return {}