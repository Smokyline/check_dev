from django.urls import path, include
from app.views import post_dev_status, get_dev_status, index

urlpatterns = [
    path('', index, name='index'),
    path('post-status/', post_dev_status, name='post-status'),
    path('get-status/', get_dev_status, name='get-status'),
]
