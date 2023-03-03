from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from psycopg2 import IntegrityError
from Documents.models import Documento, Tipodocumento
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from core.forms import *
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
    
    modal=  ["Registro de usuario","¿Desea guardar los datos?","No","Guardar"]
    
    if request.method == 'GET':
        return render(
            request,
            'core/signup.html',
            {
            'modal':modal
                
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
    
    todo_seleccionado = request.GET.get('allSelected')

    documentosMarcados = request.GET.getlist('activo') 
    documentosMarcadosDos = request.GET.getlist('activo') 

    for tipo in tipos:
        tipo.activado = True

    if (todo_seleccionado == "true"):
            for tipo in tipos:
                documentosMarcados.append(tipo.idtipodocumento)

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



    if (todo_seleccionado == "true"):
        if documentosMarcadosDos:
            for tipo in tipos:
                encontrado = False
                for idtipo in documentosMarcadosDos:
                    if  tipo.idtipodocumento == int(idtipo):
                        encontrado = True
                tipo.activado = encontrado        
    else:
        todo_seleccionado = "false"

    max_elements_per_page = 6

    paginator = Paginator(docs, max_elements_per_page)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    div_agregar= []
    if max_elements_per_page % 2 != 0:
        max_elements_per_page = max_elements_per_page + 2
    div_agregar.append(range(max_elements_per_page-len(docs)))
    return  render(request,'core/home.html',{'todo_seleccionado': todo_seleccionado, 'div_agregar': div_agregar, 'texto':texto, 'docs':page_obj, 'categories': tipos, 'page_obj': page_obj, 'searchKey': searchKey})

def users (request): 
    if request.user.type == 'ADM':
        users = User.objects.all()
        return render(request,'core/users.html',{'users':users})
    else: return redirect('home')
    
    
# def editUser(request, id):
#     modal=  ["Editar documento","¿Desea guardar cambios?","Cancelar","Guardar"]
#     if request.user.is_superuser:
#         user = User.objects.get(id=id)
        
#         return render(request,'core/editUser.html',{'user':user})
    

def myProfile(request):
    modal=  ["Modificar usuario","¿Desea guardar cambios?","Cancelar","Modificar"]
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.get(id=request.user.id)
            user.first_name = request.POST.get("name", "default value")
            user.last_name = request.POST.get("lastname", "default value")
            user.email = request.POST.get("email", "default value")
            user.username = request.POST.get("username", "default value")
            user.set_password(request.POST.get("password1", "default value"))
            user.save()
            messages.add_message(request, messages.INFO, 'Usuario modificado correctamente')
            
            return redirect('home')
        
        else: 
            return render(request,'core/home.html',{'user':user, 'modal':modal})

    
        
    else:
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            return render(request,'core/myProfile.html',{'user':user,  'modal':modal})
        else:
            return render(request,'core/login.html',{'form': AuthenticationForm})

def createUser(request):
    modal=  ["Crear Usuario","¿Desea guardar cambios?","Cancelar","Guardar"]
    
    frm = FrmCreateUser
    if request.method ==  'POST':
        frm = FrmCreateUser(request.POST)
        if frm.is_valid():
            
            frm.cleaned_data["password"] = User.set_password(request.POST.get("password", "default value"))
            
            frm.save()  
                   
            messages.add_message(request, messages.SUCCESS, 'Usuario creado correctamente')
            return redirect('home')
        else:
            return render(request,'core/createUser.html',{'form':frm, 'modal':modal})
    else:
        return render(request,'core/createUser.html',{'form':frm, 'modal':modal})
    
def modifyUser(request, id):
    modal=  ["Crear Usuario","¿Desea guardar cambios?","Cancelar","Guardar"]
    
    user = User.objects.get(id=id)
    frm = FrmCreateUser(instance=user)
    
    if request.method ==  'POST':
        frm = FrmCreateUser(request.POST)
        if frm.is_valid():
            userActual = User.objects.get(id=id)

            passwordEdit = userActual.password
            print("NUEVA CONTRASENIA = ", request.POST.get("password"))
            print("NUEVA CONTRASENIA = ", request.POST.get("password"))
            print("NUEVA CONTRASENIA = ", request.POST.get("password"))
            print("NUEVA CONTRASENIA = ", request.POST.get("password"))
            print("NUEVA CONTRASENIA = ", request.POST.get("password"))

            if (request.POST.get("password") != ''):
                userActual.set_password(request.POST.get("password"))
                passwordEdit= userActual.password

            user = User(id = user.id, type = request.POST.get("type", userActual.type),
                        email = request.POST.get("email", userActual.email),
                        username=request.POST.get("username", userActual.username),
                        first_name = request.POST.get("first_name", userActual.first_name),
                        last_name = request.POST.get("last_name", userActual.last_name),
                        password = passwordEdit)
            

            print(passwordEdit)
            #user.set_password(request.POST.get("password1", "default value"))
            #user.username = request.POST.get("username", "default value")
            #user.first_name = request.POST.get("first_name", "default value")
            ##user.last_name = request.POST.get("last_name", "default value")
            #user.email = request.POST.get("email", "default value")
            #user.type = request.POST.get("type", "default value")
            #user.set_password(request.POST.get("password1", "default value"))
            
            user.save()
            
            messages.add_message(request, messages.SUCCESS, 'Usuario modificado correctamente')
            return redirect('home')
        else:
            return render(request,'core/modUser.html',{'form':frm, 'modal':modal ,'id':id})
    else:
        return render(request,'core/modUser.html',{'form':frm, 'modal':modal, 'id':id})

        
        
        
    
    
