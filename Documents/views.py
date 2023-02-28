import os
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from django.http import HttpResponse, Http404
import mimetypes
from .models import Tipodocumento, Documento
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html" 


# from ..core import settings

# Create your views here.

@login_required(login_url='signin' , redirect_field_name = 'documentos')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    tipos = Tipodocumento.objects.all()
    
    if request.user.type   == 'CRE':
        documentos = Documento.objects.all().filter(usuario_id = request.user.id);
    else:  
        documentos = Documento.objects.all();
    
    
    # for doc in documentos:
    #     if doc.portada == None:
    #         tipoGEt = Tipodocumento.objects.all().filter(idtipodocumento = doc.idtipodocumento)
    #         doc.portada= tipoGEt.imagen
        
    return render(request,'documents/index_document.html', {'documentos': documentos, 'categories': tipos})


@login_required
def edit(request, codigo):
    if request.method == 'POST':        
        documentoEdit = Documento.objects.get(iddocumento = codigo)
        documentoEdit.titulo = request.POST["in_titulo"]
        
        documentoEdit.ruta = request.FILES["in_ruta"]

        tipoDoc = Tipodocumento.objects.get(idtipodocumento=request.POST["in_tipodocumento"])
        documentoEdit.idtipodocumento = tipoDoc
        documentoEdit.estado = request.POST["in_estado"]

        documentoEdit.save()

        return redirect('../../Documentos/')        
    else:
        registro = Documento.objects.get(iddocumento = codigo)
        choices = Tipodocumento.objects.all();
        estados = ["En análisis", "Aceptado", "Rechazado", "No revisado"]
        rutasDoc = os.getcwd()  + registro.ruta.url
        return render(request, 'documents/edit_document.html', {'rutasDoc':rutasDoc, 'form':frmCrearCuenta, 'registro': registro, 'codigo':codigo, 'choices':choices, 'estado':estados})


def choose_document(request):
    if request.method == 'POST':
        pass
    else:
        tipos = Tipodocumento.objects.all()
        return render(request,'documents/choose_document_type.html', {'tipos': tipos})
    
@login_required  
def get_document(request, id):
    
    if request.method == 'POST':
        pass
    else:
        registro = Documento.objects.get(iddocumento = id)
        atributos = Detalledocumento.objects.filter(iddocumento = id)
        tipodoc = Tipodocumento.objects.all()
        print(registro.ruta.url)
        return render(request,'documents/details_doc.html', {'registro': registro, 'atributos': atributos,'tipos': tipodoc})   
    
       

def createCategory(request):
    
    if request.method == 'POST':
        frm = frmCrearCategoria(request.POST, request.FILES)
        if frm.is_valid():
            frm.save()
            return redirect('documentos:documentos')
        else :
            return render(request, 'documents/createCategory.html', {'form':frm})

        
        
    else:
        frm = frmCrearCategoria
        return render(request, 'documents/createCategory.html', {'form':frm})
    
def getCategories(request):
    if(request.method == 'GET'):
        categories =Tipodocumento.objects.all();
        return render(request,'documents/documentsType.html', {'categories': categories})
    
def myDocs(request):
    if(request.method == 'GET'):
        if request.user.type   == 'CRE':
            myDocs = Documento.objects.all().filter(usuario_id = request.user.id);
        else:  
            myDocs = Documento.objects.all();
        
        return render(request, 'documents/myDocs.html', {'myDocs': myDocs})



def create(request, tipo): 
    
    if request.method == 'POST':    
        try:                       
            form = frmCrearCuenta(request.POST, request.FILES)

            if form.is_valid():
                form.instance.usuario = request.user
                form.save()
                last_doc_inserted = Documento.objects.latest('iddocumento')
                
                tipos = request.POST.getlist('tipoDato')
                nom_atributos = request.POST.getlist('atributoNom')
                valores = request.POST.getlist('atributo')    
                
                detalle_atributos = request.POST.getlist('atributoNew')
                detalle_tipo = request.POST.getlist('tipoDatoNew')
                valor_atributos = request.POST.getlist('valorNew')

                for i in range(len(tipos)):
                    detalledoc = Detalledocumento (atributo=nom_atributos[i], tipodato=tipos[i], valor=valores[i], iddocumento=last_doc_inserted)
                    detalledoc.save()

                for i in range (len(detalle_atributos)):
                    detalledoc = Detalledocumento( atributo=detalle_atributos[i], tipodato = detalle_tipo[i], valor = valor_atributos[i], iddocumento = last_doc_inserted)
                    detalledoc.save();
                
                
                
                return redirect('../../Documentos/')       
            else:
                atributosBase = Basedocumento.objects.filter(idtipodocumento=tipo)
                return render(request,'documents/create_document.html',{'form': frmCrearCuenta, 'atributosBase': atributosBase , 'tipo': tipo})
  


        except:
            
            pass
    else:
        atributosBase = Basedocumento.objects.filter(idtipodocumento=tipo)
        return render(request,'documents/create_document.html',{'form': frmCrearCuenta, 'atributosBase': atributosBase , 'tipo': tipo})

    


        
def update(request, document):
    document = {'title': 'Titulo', 'description': 'Descripcion', 'file': 'file'}
    if request.method == 'POST':
        pass
    
    return render(request,'documents/updSate.html', {'document': document})

def descargar_archivo(request, archivo):
    # Obtiene la ruta completa del archivo en la carpeta media
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, archivo)
    # Verifica si el archivo existe
    if os.path.exists(ruta_archivo):
        # Abre el archivo en modo de lectura binaria
        with open(ruta_archivo, 'rb') as archivo_descarga:
            # Crea una respuesta HTTP para el archivo
            response = HttpResponse(archivo_descarga.read(), content_type='application/octet-stream')
            # Establece el encabezado de Content-Disposition para descargar el archivo
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(ruta_archivo))
            return response
    else:
        # Si el archivo no existe, levanta una excepción Http404
        raise Http404("El archivo no existe")
    
    
def edit_category(request, id):
    if request.method == 'POST':
        pass
    else:
        registro = Tipodocumento.objects.get(idtipodocumento = id)
        return render(request, 'documents/edit_category.html', {'registro': registro, 'id':id})