from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from psycopg2 import IntegrityError
from Documents.models import Documento, Tipodocumento
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import os

def signin(request):
    if request.method == 'GET':
        return render(request,'core/login.html',{'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user is None:
            return render(request,'core/login.html',{'form': AuthenticationForm,'error': 'El usuario y la contrasenia son incorrectos'})
        else:
            login(request, user)
            return redirect('home')


def signup (request):
    if request.method == 'GET':
        return render(
            request,
            'core/signup.html',
            {
                'form': UserCreationForm
            }
        )
              
    else:
        if request.POST['password1'] == request.POST['password2']:
                # registrar usuario
                user = User.objects.create_user(
                    username=request.POST.get("username", "default value"),
                    password=request.POST.get('password1', "default value")
                    
                )
                user.is_active = True
                user.is_superuser = True
                user.save()
                return redirect('home')
                
                # return render(
                #     request,
                #     'core/signup.html',
                #     {
                #         'form': UserCreationForm,
                #         'error': 'Ya existe el usuario'
                #     }
                # )
        else:
            return render(
                request,
                'core/signup.html',
                {
                    'form': UserCreationForm,
                    'error': 'Las contrasenias no coinciden'
                }
        )    

def signout(request):
        logout(request)
        return render(request,'core/login.html')


@login_required(login_url='signin')
def home(request):
    tipos = Tipodocumento.objects.all()
    if request.method == 'POST':
        #Obtener los toggle buttons que fueron activados
        documentosMarcados = request.POST.getlist('activo')           

        #Obtener los documentos que contienen el texto buscado y las categorías seleccionadas
        documentos = Documento.objects.filter(titulo__contains = request.POST.get("texto"), idtipodocumento__in = documentosMarcados)

        #Verificar que exista la imágen de los documentos, si no existe usar la de la categoría.
        for doc in documentos:        
            if(doc.portada):
                if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                    doc.portada = doc.idtipodocumento.imagen
            else:
                doc.portada = doc.idtipodocumento.imagen       

        tipos.aget_or_create('activado')
        for tipo in tipos:
            for idtipo in documentosMarcados:
                if  tipo.idtipodocumento == int(idtipo):
                    tipo.activado = True

        paginator = Paginator(documentos, 5)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)

        return render(request, 'core/home.html', {'docs': page_obj, 'categories': tipos, 'docSeleccionado': documentosMarcados, 'page_obj': page_obj})
    else:
        #Home muestra los documentos que fueron establecidos:      
        docs = Documento.objects.all()

        for doc in docs:        
            if(doc.portada):
                if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                    doc.portada = doc.idtipodocumento.imagen
            else:
                doc.portada = doc.idtipodocumento.imagen       
                
        tipos.aget_or_create('activado')
        for tipo in tipos:
            tipo.activado = True

        paginator = Paginator(docs, 5)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)

        return  render(request,'core/home.html',{'docs':page_obj, 'categories': tipos, 'page_obj': page_obj})
