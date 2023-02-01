from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('push/', push_edit, name='push'),
]
