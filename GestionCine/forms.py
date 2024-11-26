from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
#from bootstrap_datepicker_plus.widgets import DatePickerInput


class ClienteModelForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni','nombre','apellidos','email']
        labels = {
            "dni":("DNI del cliente"),
        }

        
    def clean(self):
        super().clean()


        dni = self.cleaned_data.get('dni')
        nombre = self.cleaned_data.get('nombre')
        apellidos = self.cleaned_data.get('apellidos')
        email = self.cleaned_data.get('email')
        
        clienteDni = Cliente.objects.get(dni=dni)
        if (not clienteDni is None):
            self.add_error('dni','Ya existe un cliente con ese DNI')
        
        #El nombre debe tener más de un caracter
        if len(nombre) == 1:
            self.add_error('nombre','Al menos debe tener 2 caracteres')
            
        return self.cleaned_data