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

        
        clienteDni = Cliente.objects.filter(dni=dni).first()
        if (not clienteDni is None):
            self.add_error('dni','Ya existe un cliente con ese DNI')
        
        #El nombre debe tener más de un caracter
        if len(nombre) == 1:
            self.add_error('nombre','Al menos debe tener 2 caracteres')
            
        return self.cleaned_data
    
    
    
    
class SocioModelForm(ModelForm):
    class Meta:
        model = Socio
        fields = ['numSocio','fechaAlta','fechaCaducidad','cliente']
        labels = {
                "numSocio": ("Número de socio"),
         }
        widgets = {
                "fechaAlta":forms.SelectDateWidget(),
                "fechaCaducidad":forms.SelectDateWidget(),
        }
        localized_fields = ["fechaAlta","fechaCaducidad"],
    
    
    def clean(self):
        super().clean()
        
        numSocio = self.cleaned_data.get('numSocio')
        fechaAlta = self.cleaned_data.get('fechaAlta')
        fechaCaducidad = self.cleaned_data.get('fechaCaducidad')
        
        socioNum = Socio.objects.filter(numSocio=numSocio).first()
        if(not socioNum is None):
            self.add_error('numSocio','Ya hay un socio con ese número')
            
        #La fecha de alta tiene que ser anterior a hoy y la de caducidad posterior
        fechaHoy=date.today()
        if fechaHoy < fechaAlta :
            self.add_error('fechaAlta','La fecha de alta debe ser menor a hoy')
            
        if fechaHoy > fechaCaducidad :
            self.add_error('fechaCaducidad','La fecha de caducidad debe ser mayor a hoy')
        
        return self.cleaned_data