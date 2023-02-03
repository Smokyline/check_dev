from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.db import transaction
# Create your views here.
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from app.app_logic_foo import *
from check_dev.settings import BASE_DIR
# Create your views here.

def index(request):
    f = open(os.path.join(BASE_DIR, 'readme.txt'), 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

@csrf_exempt
def post_dev_status(request):
    request_dict = json.loads(request.body, strict=False)
    posting_status = post_in_sql_dev_status(request_dict)
    if posting_status:
        return JsonResponse({'status': 0}, safe=False)
    else:
        return JsonResponse({'status': 1}, safe=False)

@csrf_exempt
def get_dev_status(request):
    request_dict = json.loads(request.body)
    status_dict = get_from_sql_dev_status(request_dict)
    return JsonResponse(status_dict, safe=False)

@csrf_exempt
def get_last_dev_status(request):
    request_dict = json.loads(request.body)
    last_status_dict = get_last_dev_status_from_sql(request_dict)
    return JsonResponse(last_status_dict, safe=False)
