from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from psycopg2 import IntegrityError
from Documents.models import Documento, Tipodocumento
from django.contrib.auth.decorators import login_required

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
    docs = Documento.objects.all()


    # if request.user.type == 'ADM':
    #     docs = Documento.objects.all()
    # elif  request.user.type == 'CRE':
    #     docs = Documento.objects.all().filter(publico = 1, estado  = 'AUT')

    if request.method == 'GET':
        
        return  render(request,'documents/docs_content.html',{'docs':docs, 'categories': tipos})
    else:
        search = request.POST.get('search')
        filtros = request.POST.getlist("chk")
        
        docs = docs.filter(titulo__icontains = search)

        
        for filtro in filtros:
            if filtro == '0':
                break
            else:
                # docs_aux = Documento.objects.all().filter(idtipodocumento = filtro)
                # docs = docs.union(docs_aux)
                docs = docs.filter(idtipodocumento = filtro)
        return  render(request,'documents/docs_content.html',{'docs':docs, 'categories': tipos, 'filtros': filtros, 'search': search})

        # for filtro in filtros:
        #     print(filtro)


