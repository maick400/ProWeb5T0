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
from django.contrib import messages

# from ..core import settings

# Create your views here.

@login_required(login_url='signin' , redirect_field_name = 'documentos')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    tipos = Tipodocumento.objects.all() 
    #Home muestra los documentos que fueron establecidos:      
    docs = Documento.objects.all()
    docs  = Documento.objects.all().filter(usuario=request.user.id)
    searchKey = request.POST.get("key", "searchKey")
    
    for doc in docs:        
        if(doc.portada):
            if(os.path.exists(os.getcwd() + doc.portada.url) == False):
                doc.portada = doc.idtipodocumento.imagen
        else:
            doc.portada = doc.idtipodocumento.imagen
            
    texto = request.GET.get('texto')

    todo_seleccionado = request.GET.get("allSelected")

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

@login_required
def edit(request, codigo):
    registro = Documento.objects.get(iddocumento = codigo)
    choices = Tipodocumento.objects.all();
    atributosDocumento = Detalledocumento.objects.filter(iddocumento = codigo);
    estados = ["En análisis", "Aceptado", "Rechazado", "No revisado"]
    tiposAtributos = TIPOS_ATRIBUTO

    if request.method == 'POST':        
        documentoEdit = Documento.objects.get(iddocumento = codigo)
        estadoDocumentoAnterior = documentoEdit.estado

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

        valor_atributosTextArea = request.POST.getlist('valorModificadoTextArea')


        valor_atributos = request.POST.getlist('valorModificado')

        ids_detalles = request.POST.getlist('idsDetalle')

        detalle_atributos_Nuevo = request.POST.getlist('atributoNew')
        detalle_tipo_Nuevo = request.POST.getlist('tipoDatoNew')
        valor_atributos_Nuevo = request.POST.getlist('valorNew')
        valor_atributos_NuevoTextArea = request.POST.getlist('valorNewTextArea')

        
        for i in range (len(ids_detalles)):   
            if (detalle_tipo[i] == 'textarea'):
                detalleEditar = Detalledocumento(id=ids_detalles[i], atributo=detalle_atributos[i], tipodato = detalle_tipo[i], valor = valor_atributosTextArea[i], iddocumento = documentoEdit)            
            else:
                detalleEditar = Detalledocumento(id=ids_detalles[i], atributo=detalle_atributos[i], tipodato = detalle_tipo[i], valor = valor_atributos[i], iddocumento = documentoEdit)            

            print(detalle_atributos[i])
            ids_detallesOriginal.remove(ids_detalles[i]);
            detalleEditar.save()
        
        print (valor_atributos_NuevoTextArea, detalle_tipo)
        for i in range (len(valor_atributos_Nuevo)):           
            if(detalle_tipo_Nuevo[i] == 'textarea'):
                detalleEditar = Detalledocumento( atributo=detalle_atributos_Nuevo[i], tipodato = detalle_tipo_Nuevo[i], valor = valor_atributos_NuevoTextArea[i], iddocumento = documentoEdit )
            else:
                detalleEditar = Detalledocumento( atributo=detalle_atributos_Nuevo[i], tipodato = detalle_tipo_Nuevo[i], valor = valor_atributos_Nuevo[i], iddocumento = documentoEdit )
                
            detalleEditar.save();

        for i in range  (len(ids_detallesOriginal)):
            detalleEliminar = Detalledocumento.objects.get(id = ids_detallesOriginal[i]);
            detalleEliminar.delete();
        
        #Verificar que quien lo revise sea un administrador o analista
        
        if request.POST.get("in_estado") != estadoDocumentoAnterior:            
            if(request.user.type == 'ADM' or request.user.type == 'ANA'):
                documentoEdit.usuarioanalista_id = request.user.id            
        

        documentoEdit.save()

        return redirect('documentos:documentos')        
    else:
        
        return render(request, 'documents/edit_document.html', {'tAtributos': tiposAtributos, 'frmAtributos':frmDetalleDocumento, 'form':frmCrearCuenta, 'registro': registro, 'codigo':codigo, 'choices':choices, 'estado':estados, 'atributosDocumento':atributosDocumento})


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

    
        if(registro.portada):
            if(os.path.exists(os.getcwd() + registro.portada.url) == False):
                registro.portada = registro.idtipodocumento.imagen
        else:
            registro.portada = registro.idtipodocumento.imagen
        if registro.portada is None:
            registro.portada = registro.idtipodocumento.imagen

        i = 0;
        #Obtener otros documentos:
        docsAlt = Documento.objects.all().order_by("iddocumento")
        docsAlt.aget_or_create('columnNumberAdd')

        fileSize = 0

        for doc in docsAlt:                        
            doc.columnNumber = (doc.iddocumento % 3) + i
            if(doc.portada):
                if (os.path.exists(os.getcwd() + doc.portada.url) == False):
                    doc.portada = doc.idtipodocumento.imagen
                else:
                    fileSize = round(os.path.getsize(os.getcwd() + registro.ruta.url) * 10**-6, 2)
            else:
                doc.portada = doc.idtipodocumento.imagen
               

        paginator = Paginator(docsAlt, 3)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        
        columnsToAdd = []       
        if len(docsAlt)  % 2 == True:
            columnsToAdd.append(range(2))
        else:
            columnsToAdd.append(range(1))

        return render(request,'documents/details_doc.html', {'fileSize': fileSize, 'registro': registro, 'atributos': atributos,'tipos': tipodoc, 'docsAlt': page_obj, 'page_obj': page_obj, 'columnsToAdd': columnsToAdd})   
      

def createCategory(request):    
    modal=  ["Editar documento","¿Desea guardar cambios?","Cancelar","Guardar"]

    if request.method == 'POST':
        frm = frmCrearCategoria(request.POST, request.FILES)
        
        if frm.is_valid():
            frm.save()
            messages.add_message(request, messages.SUCCESS, 'Categoria creada exitosamente')

            last_cat = Tipodocumento.objects.last()
            
            detalle_atributos_Nuevo = request.POST.getlist('atributoNew')
            detalle_tipo_Nuevo = request.POST.getlist('tipoDatoNew')
            
            
            for i in range (len(detalle_atributos_Nuevo)):
                base_doc = Basedocumento(idtipodocumento = last_cat, atributo = detalle_atributos_Nuevo[i], tipodato = detalle_tipo_Nuevo[i])
                base_doc.save()
            frm.save()
            return redirect('documentos:categories')
        else :            
            return render(request, 'documents/createCategory.html', {'modal':modal, 'tAtributos': tiposAtributos, 'frmAtributos':frmDetalleDocumento, 'form':frm})

        
        
    else:
        frm = frmCrearCategoria
        tiposAtributos = TIPOS_ATRIBUTO
        return render(request, 'documents/createCategory.html', {'modal':modal, 'tAtributos': tiposAtributos, 'frmAtributos':frmDetalleDocumento, 'form':frm})

        # return render(request, 'documents/createCategory.html', {'form':frm})
    
def getCategories(request):
    if(request.method == 'GET'):        
        categories =Tipodocumento.objects.all()

        return render(request,'documents/documentsType.html', {'categories': categories})
    

    

def editCategory(request, id):   
    tiposAtributos = TIPOS_ATRIBUTO
    if request.method == 'POST':
        categories = Tipodocumento.objects.get(idtipodocumento = id)
        detalleCategoria = Basedocumento.objects.filter(idtipodocumento = id)

        tipo_dato_modificado = request.POST.getlist("tipoDatoModificado")
        ids_detalles = request.POST.getlist("idsDetalle")
        detalle_atributos = request.POST.getlist('atributoModificado')
        ids_detallesOriginal = request.POST.getlist('idsDetalleOriginal')

        atributosNew = request.POST.getlist('atributoNew')
        tipoDatoNew = request.POST.getlist("tipoDatoNew")

        for i in range (len(ids_detalles)):           
            detalleEditar = Basedocumento(id=ids_detalles[i], tipodato = tipo_dato_modificado[i],atributo=detalle_atributos[i], idtipodocumento = categories)            
            ids_detallesOriginal.remove(ids_detalles[i]);  
            detalleEditar.save();
        
        for i in range (len(tipoDatoNew)):
            detalleCrear = Basedocumento(atributo = atributosNew[i], tipodato = tipoDatoNew[i], idtipodocumento = categories)
            detalleCrear.save()

        for i in range  (len(ids_detallesOriginal)):
            detalleEliminar = Basedocumento.objects.get(id = ids_detallesOriginal[i]);
            detalleEliminar.delete();


        categories.descripcion = request.POST.get("descripcion")
        categories.tipo = request.POST.get("tipo")

        if(request.POST.get("in_ruta") == '' or request.POST.get("in_ruta") is None):
            return render(request,'documents/documentsType.html', {'categories': Tipodocumento.objects.all()})    

        categories.imagen = request.FILES["in_ruta"]

        categories.save()
        return render(request,'documents/documentsType.html', {'categories': Tipodocumento.objects.all()})    
    else:
        categories = Tipodocumento.objects.get(idtipodocumento = id)
        detalleCategoria = Basedocumento.objects.filter(idtipodocumento = id)
        return render(request,'documents/edit_category.html', {'frmDetalleDocumento': frmDetalleDocumento, 'categories': categories, 'detallesCategoria': detalleCategoria, 'tiposAtributo': tiposAtributos})



def create(request, tipo):     
    if request.method == 'POST':    
        try:                       
            form = frmCrearCuenta(request.POST, request.FILES)
            print("asdasdsds", request.POST.get("ruta"))
            if request.POST.get("ruta") == '':
                return redirect('documentos:documentos') 
            if form.is_valid():  
                form.instance.usuario = request.user
                form.save()

                last_doc_inserted = Documento.objects.latest('iddocumento')
                
                tipos = request.POST.getlist('tipoDato')
                nom_atributos = request.POST.getlist('atributoNom')
                valores = request.POST.getlist('atributo')  

                valoresTextArea = request.POST.getlist('atributoTextArea')    

                
                detalle_atributos = request.POST.getlist('atributoNew')
                detalle_tipo = request.POST.getlist('tipoDatoNew')
                valor_atributos = request.POST.getlist('valorNew')
                
                valor_atributos_NuevoTextArea = request.POST.getlist('valorNewTextArea')


                for i in range(len(tipos)):   
                    detalledoc = Detalledocumento (atributo=nom_atributos[i], tipodato=tipos[i], valor=valores[i], iddocumento=last_doc_inserted)
                  
                    detalledoc.save()

                for i in range (len(detalle_atributos)):
                    if(detalle_tipo[i] == 'textarea'):        
                        detalledoc = Detalledocumento( atributo=detalle_atributos[i], tipodato = detalle_tipo[i], valor = valor_atributos_NuevoTextArea[i], iddocumento = last_doc_inserted)
                    else:
                        detalledoc = Detalledocumento( atributo=detalle_atributos[i], tipodato = detalle_tipo[i], valor = valor_atributos[i], iddocumento = last_doc_inserted)
                    
                    detalledoc.save();
              
                return redirect('documentos:documentos')       
            
            else:
                atributosBase = Basedocumento.objects.filter(idtipodocumento=tipo)              
                return render(request,'documents/create_document.html',{'form': frmCrearCuenta, 'frmAtributos':frmDetalleDocumento, 'atributosBase': atributosBase , 'tipo': tipo})
  
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