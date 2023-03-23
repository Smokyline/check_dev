
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.db import transaction
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from app.app_logic_foo import *
from check_dev.settings import BASE_DIR
import jwt
import time
from app.logger import save_log
import logging
from logging.handlers import RotatingFileHandler
from check_dev.settings import LOGGING
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOGGING['handlers']['file']['filename'], maxBytes=1000000, backupCount=5)
logger.addHandler(handler)


# Create your views here.

def index(request):
    f = open(os.path.join(BASE_DIR, 'readme.txt'), 'r', encoding='utf-8')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain; charset=utf8")

def status(request):
    return render(request, 'last-status.html')

@csrf_exempt
def post_dev_status(request):
    """
    Постинг статуса девайса в SQL таблицу
    """
    try:
        # проверка токена
        token = str(request.headers['Authorization']).split(' ')[1]
        payload_data = jwt.decode(jwt=token, key=os.getenv('SECRET_KEY'), algorithms=['HS256', ])
    except Exception as e:
        logger.error(e)
        return HttpResponse(status=401)

    request_dict = json.loads(request.body, strict=False)
    posting_status = post_in_sql_dev_status(request_dict)
    if posting_status:
        return JsonResponse({'status': 1}, safe=False)
    else:
        return JsonResponse({'status': 0}, safe=False)





@csrf_exempt
def get_dev_status(request):
    """
    возвращает данные из таблицы за период
    """
    try:
        # проверка токена
        token = str(request.headers['Authorization']).split(' ')[1]
        payload_data = jwt.decode(jwt=token, key=os.getenv('SECRET_KEY'), algorithms=['HS256', ])
    except Exception as e:
        logger.error(e)
        return HttpResponse(status=401)
    try:
        # получение данных за период
        request_dict = json.loads(request.body)
        ip = request.META.get('HTTP_X_REAL_IP')
        save_log(time.time(), 'INFO', 'request', ip, request_dict['obs'], request_dict['dev'],
                 request_dict['date0_from'], request_dict['date0_to'])

        status_dict = get_from_sql_dev_status(request_dict)
    except Exception as e:
        logger.error(e)
        status_dict = {}
    # словарь пустой если ошибка или же за указанный период данных нет
    return JsonResponse(status_dict, safe=False)

@csrf_exempt
def get_last_dev_status(request):
    """
    возвращает последние данные
    """
    try:
        # проверка токена
        token = str(request.headers['Authorization']).split(' ')[1]
        payload_data = jwt.decode(jwt=token, key=os.getenv('SECRET_KEY'), algorithms=['HS256', ])
    except Exception as e:
        logger.error(e)
        return HttpResponse(status=401)

    # получение последних данных из таблицы
    request_dict = json.loads(request.body)
    last_status_dict = get_last_dev_status_from_sql(request_dict)
    return JsonResponse(last_status_dict, safe=False)

@csrf_exempt
def get_all_obs(request):
    """
    возвращает список всех обсерваторий и их устройств
    """
    try:
        # проверка токена
        token = str(request.headers['Authorization']).split(' ')[1]
        payload_data = jwt.decode(jwt=token, key=os.getenv('SECRET_KEY'), algorithms=['HS256', ])
    except Exception as e:
        logger.error(e)
        return HttpResponse(status=401)

    all_obs_dict = get_all_obs_from_sql()
    return JsonResponse(all_obs_dict, safe=False)

@csrf_exempt
def check_token(request):
    try:
        token = str(request.headers['Authorization']).split(' ')[1]
        payload_data = jwt.decode(jwt=token, key=os.getenv('SECRET_KEY'), algorithms=['HS256', ])
        print(payload_data)
        return HttpResponse('token verification passed')
    except Exception as e:
        return HttpResponse('token verification failed')
