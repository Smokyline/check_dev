from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('status/', status, name='status'),
    path('post-status/', post_dev_status, name='post-status'),
    path('get-status/', get_dev_status, name='get-status'),
    path('get-last-status/', get_last_dev_status, name='get-last-status'),
]
