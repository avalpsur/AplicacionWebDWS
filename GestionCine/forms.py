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
    


class PeliculaForm(forms.Form):
    titulo = forms.CharField(label="Título",
                             required=True,
                             max_length=150,
                            )
    
    director = forms.CharField(label="Director",
                               required=True,
                               max_length=100,
                               help_text="Nombre y apellido"
                               )
    

    sinopsis = forms.CharField(label="Sinopsis",
                               required=True,
                               widget=forms.Textarea()
                               )
    
    fechaLanzamiento = forms.DateField(label="Fecha de estreno",
                                       initial=datetime.date.today,
                                       widget=forms.SelectDateWidget()
                                       )
    
    tiempoProyectada = forms.DurationField(label="Duración",
                                           required=True,

                                           )
    sala = forms.ModelMultipleChoiceField(queryset=Sala.objects.all(),
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple,
                                            label="Salas disponibles"
                                        )
    def clean(self):
        super().clean()

        titulo = self.cleaned_data.get('titulo')
        director = self.cleaned_data.get('director')
        sinopsis = self.cleaned_data.get('sinopsis')
        fechaLanzamiento = self.cleaned_data.get('fechaLanzamiento')
        tiempoProyectada = self.cleaned_data.get('tiempoProyectada')
        sala = self.cleaned_data.get('sala')

        #No puede haber dos películas con el mismo título
        peliculaTitulo = Pelicula.objects.filter(titulo=titulo).first()
        if(not peliculaTitulo is None):
            self.add_error('Titulo','Ya existe una película con ese título')

        #La fecha de lanzamiento no puede ser superior a la de hoy, puesto que solo guardamos películas que ya están estrenadas
        fechaHoy = date.today()
        if fechaHoy < fechaLanzamiento :
            self.add_error('fechaLanzamiento','Solamente guardamos películas ya estrenadas')

        return self.cleaned_data
    

class BusquedaPeliculaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)

    fecha_desde = forms.DateField(label="Fecha Desde",
                                  required=False,
                                  widget=forms.SelectDateWidget(years=range(1960,2024))
                                  )

    fecha_hasta =  forms.DateField(label="Fecha Hasta",
                                   required=False,
                                   widget=forms.SelectDateWidget(years=range(1960,2024)))

    sala = forms.MultipleChoiceField(choices=Pelicula.sala,
                                     required=False,
                                     widget=forms.CheckboxSelectMultiple())
    

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get("textoBusqueda")
        fecha_desde = self.cleaned_data.get("fecha_desde")
        fecha_hasta = self.cleaned_data.get("fecha_hasta")
        sala = self.cleaned_data.get("sala")

        if(textoBusqueda == ""
           and len(sala)==0
           and fecha_desde is None
           and fecha_hasta is None
           ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('sala','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta','Debe introducir al menos un valor en un campo del formulario')
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda','Debe introducir al menos 3 caracteres')
            
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
        return self.cleaned_data
    
    
class GerenteModelForm(ModelForm):
    class Meta:
        model = Gerente
        fields = ['dni','nombre','apellidos','telefono']
        labels = {
            "dni":("DNI del gerente"),
        }
    
    def clean(self):
        dni = self.cleaned_data.get("dni")
        nombre = self.cleaned_data.get("nombre")
        apellidos = self.cleaned_data.get("apellidos")
        telefono = self.cleaned_data.get("telefono")
        
        if(not dni is None):
            self.add_error('dni','Ya hay un/a gerente con ese número')
            
        if(telefono.length > 9 or telefono.length < 1):
            self.add_error('telefono','El telefono debe tener 9 caracteres')