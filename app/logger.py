import datetime
import os
from check_dev.settings import LOG_TXT_PATH

def save_log(unix_time, *args):
    line = datetime.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    for arg in args:
        line += ' %s' % arg
    print(line)
    with open(os.path.join(LOG_TXT_PATH, 'ip_request.log'), 'a') as f:
        f.write('%s\n' % (line))
