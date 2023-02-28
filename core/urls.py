"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import *
from core import settings
from django.conf.urls.static import static

from .views import *
urlpatterns = [
    path('', home , name='home'),
    path('Admin/', admin.site.urls),
    path('Signin/', signin, name='signin'),
    path('Signup/', signup, name='signup'),
    path("Logout/",signout, name="logout"),
    path('Documentos/', include('Documents.urls'),name='documentos'),
    path('Usuarios/', include('users.urls', namespace='usuarios')),
    path('oauth/', include('social_django.urls', namespace='social')),  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# =======
# """core URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path,include
# from django.shortcuts import *
# from core import settings
# from django.conf.urls.static import static

# from .views import *
# urlpatterns = [
#     path('', home , name='home'),
#     path('Admin/', admin.site.urls),
#     path('Signin/', signin, name='signin'),
#     path('Signup/', signup, name='signup'),
#     path("Logout/",signout, name="logout"),
#     path('Documentos/', include('Documents.urls'),name='documentos'),
#     path('Usuarios/', include('users.urls', namespace='usuarios')),
#     path('usuarios/', include('users.urls', namespace='usuarios')),
#     path('oauth/', include('social_django.urls', namespace='social')),  

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# >>>>>>> master
