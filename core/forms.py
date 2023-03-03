from django import forms
from django.contrib.auth.models import User
from core.CHOICES import *

class FrmCreateUser(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','type', 'password']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email' : 'Correo Electrónico',
            'type' : 'Tipo de Usuario', 
            'password': 'Contraseña', 
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'type': forms.Select(choices=TYPE_CHOICES, attrs={'class':'form-select'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),

        }
        