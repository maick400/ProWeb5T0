from django import forms
from django.forms.models import inlineformset_factory
from .models import *
from core.choices2 import *

class frmCrearCuenta(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ('idtipodocumento','portada','titulo','ruta', 'estado', )
        labels = {
            'idtipodocumento':'Tipo de Documento',
            'portada':'Portada',
            'titulo':'Título', 
            'ruta':'Seleccionar Archivo', 
            'estado':'Estado'
        }
        
        widgets = {
            'idtipodocumento':forms.HiddenInput(),
            'titulo':forms.TextInput(attrs={ 'class':'form-control'}),
            'portada':forms.FileInput(attrs={'class':'form-control'}),
            'ruta':forms.FileInput(attrs={'class':'form-control'}), 
            'estado':forms.Select(choices=[('ABIERTO', 'ABIERTO'),('CERRADO', 'CERRADO')], attrs={'class':'form-select'})
        }
        
        
class frmDetalleDocumento(forms.ModelForm):
    class Meta:
        model = Detalledocumento
        fields = ('tipodato', )
        labels = {
           'tipodato': ''
        }
        widgets = {
            'tipodato':forms.Select(choices=TIPOS_ATRIBUTO, attrs={'class':'form-select', 'hidden': 'hidden'})
        }

class frmCrearCategoria(forms.ModelForm):
    class Meta:
        model = Tipodocumento
        fields = ('tipo' , 'imagen', 'descripcion')
        
        labels = {
            'tipo': 'Tipo de Documento',
            'imagen': 'Imagen', 
            'descripcion': 'Descripción'
        } 
        
        widgets = {
            
            'tipo': forms.TextInput(attrs={'class':'form-control'}),
            'imagen': forms.FileInput( attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'})
            
        }
        

        
# =======
# from django import forms
# from django.forms.models import inlineformset_factory
# from .models import *

# class frmCrearCuenta(forms.ModelForm):
#     class Meta:
#         model = Documento
#         fields = ('idtipodocumento','portada','titulo','ruta', 'estado', )
#         labels = {
#             'idtipodocumento':'Tipo de Documento',
#             'portada':'Portada',
#             'titulo':'Título', 
#             'ruta':'Seleccionar Archivo', 
#             'estado':'Estado'
#         }
        
#         widgets = {
#             'idtipodocumento':forms.HiddenInput(),
#             'titulo':forms.TextInput(attrs={ 'class':'form-control'}),
#             'portada':forms.FileInput(attrs={'class':'form-control'}),
#             'ruta':forms.FileInput(attrs={'class':'form-control'}), 
#             'estado':forms.Select(choices=[('ABIERTO', 'ABIERTO'),('CERRADO', 'CERRADO')], attrs={'class':'form-select'})
#         }
        
        
# class frmCrearCategoria(forms.ModelForm):
#     class Meta:
#         model = Tipodocumento
#         fields = ('tipo' , 'imagen', 'descripcion')
        
#         labels = {
#             'tipo': 'Tipo de Documento',
#             'imagen': 'Imagen', 
#             'descripcion': 'Descripción'
#         } 
        
#         widgets = {
            
#             'tipo': forms.TextInput(attrs={'class':'form-control'}),
#             'imagen': forms.FileInput( attrs={'class':'form-control'}),
#             'descripcion': forms.TextInput(attrs={'class':'form-control'})
            
#         }
        

        
# >>>>>>> master
        