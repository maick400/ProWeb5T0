from django.http import * 
from django.conf import settings
from .views import *
from django.urls import path 

app_name = 'users'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('edit/<user>/', edit, name='edit'),
    path('delete/<int:user>', delete, name='delete'),
]

 
