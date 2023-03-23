import hashlib
import pymysql
import os
import logging
from logging.handlers import RotatingFileHandler
from check_dev.settings import LOGGING
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOGGING['handlers']['file']['filename'], maxBytes=1000000, backupCount=5)
logger.addHandler(handler)

def post_in_sql_dev_status(request):
    """
    постинг в БД
    """
    obs_code = str(request['obs']).upper()
    date0 = int(request['date0'])  # unix time sec
    dev_code = str(request['dev']).upper()
    date1 = int(request['date1'])  # unix time ms
    filename = str(request['filename']).lower()
    md5_hash = hashlib.md5(str(request['md5']).encode('utf-8')).digest()  # 16 byte binary file hash


    try:
        ucount = int(request['ucount'])
    except Exception as e:
        ucount = -1

    try:
        filesize = int(request['filesize'])
    except Exception as e:
        filesize = -1

    try:
        conn = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                               user=os.getenv('SQL_USER'),
                               passwd=os.getenv('SQL_PSW'),
                               db=os.getenv('SQL_DB'),
                               charset='utf8mb4', )
        cur = conn.cursor()
        mySql_insert_query  = """INSERT %s"""%os.getenv('SQL_TABLE') +"""(obs, dev, date0, date1, filename, md5, ucount, filesize) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_tuple = (obs_code, dev_code, date0, date1, filename, md5_hash, ucount, filesize)
        cur.execute(mySql_insert_query, insert_tuple)
        conn.commit()
        conn.close()
        return 0
    except Exception as E:
        logger.error(E)
        return 1


def get_from_sql_dev_status(request):
    """
    получение данных с БД по станциям и времени
    """
    obs_code = str(request['obs']).upper()
    date0_from = int(request['date0_from'])
    date0_to = int(request['date0_to'])
    date1_from = int(request['date1_from'])
    date1_to = int(request['date1_to'])
    #filename = str(request['filename']).lower()
    dev_code = str(request['dev']).upper()
    if obs_code == 'GC0':
        try:
            1/0
        except Exception as e:
            #logger.error(e)
            #logger.error('error 1/0')
            pass

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
                           'md5': [],
                           'ucount': [],
                           'filesize': []
                           }
            for row in respond:
                # obs_code, dev_code, date0, date1, filename, md5_hash, ucount, filesize
                #    0          1       2      3        4        5        6         7
                status_dict['obs'].append(row[0])
                status_dict['dev'].append(row[1])
                status_dict['date0'].append(row[2])
                status_dict['date1'].append(row[3])
                status_dict['filename'].append(row[4])
                status_dict['md5'].append(hashlib.md5(row[5]).hexdigest())
                status_dict['ucount'].append(row[6])
                status_dict['filesize'].append(row[7])



            return status_dict
    except Exception as E:
        logger.error(E)
        return {}

def get_last_dev_status_from_sql(request):
    """
    получение словаря с последними данными по обсерватории и устройству
    """
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
            row = respond[0]
            status_dict = {'obs': row[0],
                           'dev': row[1],
                           'date0': row[2],
                           'date1': row[3],
                           'filename': row[4],
                           'md5': hashlib.md5(row[5]).hexdigest(),
                           'ucount': row[6],
                           'filesize': row[7]
                           }
            return status_dict
    except Exception as E:
        logger.error(E)
        return {}

def get_all_obs_from_sql():
    """
    получение списка всех доступных обсерваторий
    """
    try:
        db = pymysql.connect(host=os.getenv('SQL_HOST'), port=3306,
                             user=os.getenv('SQL_USER'),
                             passwd=os.getenv('SQL_PSW'),
                             db=os.getenv('SQL_DB'),
                             charset='utf8mb4', )
        request_to_sql = """SELECT DISTINCT obs FROM %s;""" % (os.getenv('SQL_TABLE'))
        cur = db.cursor()
        cur.execute(request_to_sql)
        respond = cur.fetchall()
        db.close()
        if len(respond) == 0:
            return {}
        else:
            all_obs_dist = {'obs_list': [obs[0] for obs in respond]}
            return all_obs_dist
    except Exception as E:
        logger.error(E)
        return {}