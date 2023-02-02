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
        mySql_insert_query  = """INSERT %s"""%os.getenv('SQL_TABLE') +"""(obs, dev, date0, date1, filename, md5) VALUES (%s, %s, %s, %s, %s, %s)"""
        insert_tuple = (obs_code, dev_code, date0, date1, filename, md5_hash)
        cur.execute(mySql_insert_query, insert_tuple)
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
    #filename = str(request['filename']).lower()
    dev_code = str(request['dev']).upper()

    try:

        db = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                             user=os.getenv('SQL_USER'),
                             passwd=os.getenv('SQL_PSW'),
                             db=os.getenv('SQL_DB'),
                             charset='utf8mb4', )

        request_to_sql = "SELECT * FROM %s WHERE obs='%s' AND dev='%s' AND " \
                  "date0 BETWEEN %s AND %s AND date1 BETWEEN %s AND %s" % (
                      os.getenv('SQL_TABLE'), obs_code, dev_code,
                      date0_from, date0_to, date1_from, date1_to)
        print(request_to_sql)
        cur = db.cursor()
        cur.execute(request_to_sql)
        respond = cur.fetchall()
        db.close()
        print(respond)
        print(type(respond))
        if len(respond) == 0:
            return {}
        else:
            status_dict = {'obs': [],
                           'date0': [],
                           'dev': [],
                           'date1': [],
                           'filename': [],
                           'md5': []
                           }
            for row in respond:
                # obs_code, dev_code, date0, date1, filename, md5_hash
                #    0          1       2      3        4        5
                status_dict['obs'].append(row[0])
                status_dict['dev'].append(row[1])
                status_dict['date0'].append(row[2])
                status_dict['date1'].append(row[3])
                status_dict['filename'].append(row[4])
                status_dict['md5'].append(hashlib.md5(row[5]).hexdigest())

            return status_dict
    except Exception as E:
        print(E)
        return {}

def get_last_dev_status_from_sql(request):
    obs_code = str(request['obs']).upper()
    dev_code = str(request['dev']).upper()

    try:
        db = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                             user=os.getenv('SQL_USER'),
                             passwd=os.getenv('SQL_PSW'),
                             db=os.getenv('SQL_DB'),
                             charset='utf8mb4', )
        request_to_sql = """SELECT * FROM %s WHERE obs='%s' AND dev='%s' ORDER BY date0 DESC LIMIT 1""" \
                         % (os.getenv('SQL_TABLE'), obs_code, dev_code)
        cur = db.cursor()
        cur.execute(request_to_sql)
        respond = cur.fetchall()
        db.close()

        if len(respond) == 0:
            return {}
        else:
            status_dict = {'obs': [],
                           'date0': [],
                           'dev': [],
                           'date1': [],
                           'filename': [],
                           'md5': []
                           }
            row = respond[0]
            status_dict['obs'].append(row[0])
            status_dict['dev'].append(row[1])
            status_dict['date0'].append(row[2])
            status_dict['date1'].append(row[3])
            status_dict['filename'].append(row[4])
            status_dict['md5'].append(hashlib.md5(row[5]).hexdigest())
            return status_dict
    except Exception as E:
        print(E)
        return {}