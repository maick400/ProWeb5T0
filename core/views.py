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
                user.first_name = request.POST.get("name", "default value")
                user.last_name = request.POST.get("lastname", "default value")
                user.email = request.POST.get("email", "default value")
                user.is_active = True
                user.is_superuser = True
                
                if not request.user.is_superuser:
                    user.type = 'CRE'
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
    #Home muestra los documentos que fueron establecidos:      
    docs = Documento.objects.all()

    searchKey = request.POST.get("key", "searchKey")
    
    for doc in docs:        
        if(doc.portada):
            if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                doc.portada = doc.idtipodocumento.imagen
        else:
            doc.portada = doc.idtipodocumento.imagen
            
    texto = request.GET.get('texto')

    documentosMarcados = request.GET.getlist('activo') 
    for tipo in tipos:
        tipo.activado = True

    if documentosMarcados:
        for tipo in tipos:
            encontrado = False
            for idtipo in documentosMarcados:
                if  tipo.idtipodocumento == int(idtipo):
                    encontrado = True
            tipo.activado = encontrado            
    
    searchKey = request.GET.get("key", "searchKey")
    if not documentosMarcados:
        for tipo in tipos:
            documentosMarcados.append(tipo.idtipodocumento)
    
    if texto != None:
        docs = docs.filter(titulo__contains = texto, idtipodocumento__in = documentosMarcados)
    else:
        texto = ""
        docs = docs.filter(titulo__contains = "", idtipodocumento__in = documentosMarcados)

    #Verificar que exista la imágen de los documentos, si no existe usar la de la categoría.
    for doc in docs:
        if(doc.portada):
            if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                doc.portada = doc.idtipodocumento.imagen
        else:
            doc.portada = doc.idtipodocumento.imagen 

    max_elements_per_page = 6

    paginator = Paginator(docs, max_elements_per_page)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    div_agregar= []
    if max_elements_per_page % 2 != 0:
        max_elements_per_page = max_elements_per_page + 2
        
    return  render(request,'core/home.html',{'div_agregar': div_agregar, 'texto':texto, 'docs':page_obj, 'categories': tipos, 'page_obj': page_obj, 'searchKey': searchKey})


def users (request): 
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request,'core/users.html',{'users':users})
    
def editUser(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        
        return render(request,'core/editUser.html',{'user':user})
    

def myProfile(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.get(id=request.user.id)
            user.first_name = request.POST.get("name", "default value")
            user.last_name = request.POST.get("lastname", "default value")
            user.email = request.POST.get("email", "default value")
            user.username = request.POST.get("username", "default value")
            user.set_password(request.POST.get("password1", "default value"))
            user.save()
            
            return render(request,'core/home.html',{'user':user})
        
        else: 
            return render(
                request,
                'core/myProfile.html',
                {
                    'form': UserCreationForm,
                    'error': 'Las contrasenias no coinciden'
                })
    
        
    else:
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            return render(request,'core/myProfile.html',{'user':user})
        else:
            return render(request,'core/login.html',{'form': AuthenticationForm})
    