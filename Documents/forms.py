from django import forms
from django.forms.models import inlineformset_factory
from .models import *

class frmCrearCuenta(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ('idtipodocumento','portada','titulo','ruta','usuario' )
        labels = {
            'idtipodocumento':'Tipo de Documento',
            'portada':'Portada',
            'titulo':'Título', 
            'Archivo':'Seleccionar Archivo', 
            'usuario':'Usuario',
            'estado':'Estado'
        }
        
        widgets = {
            'idtipodocumento':forms.HiddenInput(),
            'titulo':forms.TextInput(attrs={ 'class':'form-control'}),
            'portada':forms.FileInput( attrs={'class':'form-control', 'accept':'image/*' }),
            'ruta':forms.FileInput(attrs={'class':'form-control', 'accept':'image/*,.pdf' }), 
            'usuario': forms.HiddenInput(),
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
        

        
        