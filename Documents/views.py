import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.core.files import File
from core import settings
from .forms import *
from django.http import HttpResponse, Http404
import mimetypes
from .models import Tipodocumento, Documento
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from core.choices2 import *
from django.core.paginator import Paginator

# from ..core import settings

# Create your views here.

@login_required(login_url='signin' , redirect_field_name = 'documentos')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    tipos = Tipodocumento.objects.all()
    if request.method == 'POST':
        #Obtener los toggle buttons que fueron activados
        documentosMarcados = request.POST.getlist('activo')           
        documentosall= Documento.objects.all().filter(usuario=request.user.id)

        #Obtener los documentos que contienen el texto buscado y las categorías seleccionadas
        documentos = documentosall.filter(titulo__contains = request.POST.get("texto"), idtipodocumento__in = documentosMarcados)

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


        return render(request,'documents/index_document.html', {'docSeleccionado': documentosMarcados, 'documentos': page_obj, 'categories': tipos, 'page_obj': page_obj})
    else:
        if request.user.type   == 'CRE':
            documentos = Documento.objects.all().filter(usuario_id = request.user.id);
        else:  
            documentos = Documento.objects.all();
        
        for doc in documentos:        
            if(doc.portada):
                if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                    doc.portada = doc.idtipodocumento.imagen
            else:
                doc.portada = doc.idtipodocumento.imagen       
                
        tipos.aget_or_create('activado')
        for tipo in tipos:
            tipo.activado = True
            
        paginator = Paginator(documentos, 5)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)

        return render(request,'documents/index_document.html', {'documentos': page_obj, 'categories': tipos, 'page_obj': page_obj})


@login_required
def edit(request, codigo):
    registro = Documento.objects.get(iddocumento = codigo)
    choices = Tipodocumento.objects.all();
    atributosDocumento = Detalledocumento.objects.filter(iddocumento = codigo);
    estados = ["En análisis", "Aceptado", "Rechazado", "No revisado"]
    tiposAtributos = TIPOS_ATRIBUTO

    if request.method == 'POST':        
        

        documentoEdit = Documento.objects.get(iddocumento = codigo)
        documentoEdit.titulo = request.POST["in_titulo"]
        
        if(request.POST.get("in_ruta") == ''):
            print("No Válido")
        else:
            print("Válido")
            documentoEdit.ruta = request.FILES["in_ruta"]

        tipoDoc = Tipodocumento.objects.get(idtipodocumento=request.POST["in_tipodocumento"])
        documentoEdit.idtipodocumento = tipoDoc
        documentoEdit.estado = request.POST["in_estado"]

        ids_detallesOriginal = request.POST.getlist('idsDetalleOriginal')

        detalle_atributos = request.POST.getlist('atributoModificado')
        detalle_tipo = request.POST.getlist('tipoModificado')
        valor_atributos = request.POST.getlist('valorModificado')
        ids_detalles = request.POST.getlist('idsDetalle')

        detalle_atributos_Nuevo = request.POST.getlist('atributoNew')
        detalle_tipo_Nuevo = request.POST.getlist('tipoDatoNew')
        valor_atributos_Nuevo = request.POST.getlist('valorNew')

        for i in range (len(ids_detalles)):           
            detalleEditar = Detalledocumento(id=ids_detalles[i], atributo=detalle_atributos[i], tipodato = detalle_tipo[i], valor = valor_atributos[i], iddocumento = documentoEdit)
            
            ids_detallesOriginal.remove(ids_detalles[i]);
            detalleEditar.save();
        
        for i in range (len(valor_atributos_Nuevo)):           
            detalleEditar = Detalledocumento( atributo=detalle_atributos_Nuevo[i], tipodato = detalle_tipo_Nuevo[i], valor = valor_atributos_Nuevo[i], iddocumento = documentoEdit )
            detalleEditar.save();

        for i in range  (len(ids_detallesOriginal)):
            detalleEliminar = Detalledocumento.objects.get(id = ids_detallesOriginal[i]);
            detalleEliminar.delete();
        

        documentoEdit.save()

        return redirect('../../Documentos/')        
    else:      
        return render(request, 'documents/edit_document.html', {'tAtributos': tiposAtributos, 'frmAtributos':frmDetalleDocumento, 'form':frmCrearCuenta, 'registro': registro, 'codigo':codigo, 'choices':choices, 'estado':estados, 'atributosDocumento':atributosDocumento})


def choose_document(request):
    if request.method == 'POST':
        pass
    else:
        tipos = Tipodocumento.objects.all()
        return render(request,'documents/choose_document_type.html', {'tipos': tipos})
    
@login_required  

@login_required  

@login_required  
def get_document(request, id):    
    if request.method == 'POST':
        pass
    else:
        registro = Documento.objects.get(iddocumento = id)
        atributos = Detalledocumento.objects.filter(iddocumento = id)
        tipodoc = Tipodocumento.objects.all()

        #Verificar que exista la portada para el registro seleccionado
        if(registro.portada):
            #Verificar que exista el archivo en la carpeta donde se almacenan las rutas
            #Si no existe el imagen para la portada del documento asignar la de la categoría
            if(os.path.exists(os.getcwd() + registro.portada.url) == False):
                registro.portada = registro.idtipodocumento.imagen
        else:
            registro.portada = registro.idtipodocumento.imagen     

        i = 0;
        #Obtener otros documentos:
        docsAlt = Documento.objects.all().order_by("iddocumento")
        cadena = ""
        docsAlt.aget_or_create('columnNumberAdd')
        
        for doc in docsAlt:                        
                doc.columnNumber = (doc.iddocumento % 3) + i
                if(doc.portada):
                     if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                        doc.portada = doc.idtipodocumento.imagen
                else:
                    doc.portada = doc.idtipodocumento.imagen
                i = i + 1
               

        paginator = Paginator(docsAlt, 3)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        
        columnsToAdd = []
       
        columnsToAdd.append(range((len(docsAlt) + 1) % 3))
            

        return render(request,'documents/details_doc.html', {'registro': registro, 'atributos': atributos,'tipos': tipodoc, 'docsAlt': page_obj, 'page_obj': page_obj, 'columnsToAdd': columnsToAdd})   
    
       

def createCategory(request):
    
    if request.method == 'POST':
        frm = frmCrearCategoria(request.POST, request.FILES)
        
        if frm.is_valid():
            frm.save()
            
            last_cat = Tipodocumento.objects.last()
            
            detalle_atributos_Nuevo = request.POST.getlist('atributoNew')
            detalle_tipo_Nuevo = request.POST.getlist('tipoDatoNew')
            
            
            for i in range (len(detalle_atributos_Nuevo)):
                base_doc = Basedocumento(idtipodocumento = last_cat, atributo = detalle_atributos_Nuevo[i], tipodato = detalle_tipo_Nuevo[i])
                base_doc.save()
            frm.save()
            return redirect('documentos:documentos')
        else :
            
            return render(request, 'documents/createCategory.html', {'form':frm})

        
        
    else:
        frm = frmCrearCategoria
        tiposAtributos = TIPOS_ATRIBUTO
        return render(request, 'documents/createCategory.html', {'tAtributos': tiposAtributos, 'frmAtributos':frmDetalleDocumento, 'form':frm})

        # return render(request, 'documents/createCategory.html', {'form':frm})
    
def getCategories(request):
    if(request.method == 'GET'):
        
        categories =Tipodocumento.objects.all();
        return render(request,'documents/documentsType.html', {'categories': categories})
    
def editCategory(request):
    pass
    


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
            print("ERRROR")           
            pass
    else:
        atributosBase = Basedocumento.objects.filter(idtipodocumento=tipo)
        return render(request,'documents/create_document.html',{'form': frmCrearCuenta, 'frmAtributos':frmDetalleDocumento, 'atributosBase': atributosBase , 'tipo': tipo})

    


        
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