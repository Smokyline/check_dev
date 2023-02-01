from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
# Create your views here.
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return HttpResponse("Hello, curious.")

@csrf_exempt
def post_status(request):



    return HttpResponse("OK")