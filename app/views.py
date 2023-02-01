from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.db import transaction
# Create your views here.
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from app_logic_foo import *
# Create your views here.

def index(request):
    return HttpResponse("Hello, curious.")

@csrf_exempt
def post_dev_status(request):
    request = json.loads(request.body)
    posting_status = post_in_sql_dev_status(request)
    if posting_status:
        return HttpResponse("OK")
    else:
        return HttpResponse("NOT OK")

def get_dev_status(request):
    request = json.loads(request.body)
    status_dict = get_dev_status(request)
    if len(status_dict) > 0:
        return JsonResponse(status_dict, safe=False)
    else:
        return Http404
