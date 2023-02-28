from django.http import * 
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path 
from .views import *


app_name = 'documentos'

urlpatterns = [
     path('', index, name="documentos"),
     path('create/<tipo>', create, name='create'),
     path('choose/', choose_document, name='chooseType'),
     path('edit/<codigo>', edit, name='edit'),
     path('details/<id>', get_document, name='details'),
     path('createCategory/', createCategory, name='createCategory'),
     path('categories/', getCategories, name='categories'),
     path('search/', getCategories, name='categories')
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


