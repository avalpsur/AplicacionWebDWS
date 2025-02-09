from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm

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
    
    
class BusquedaClienteForm(forms.Form):

        textoBusqueda = forms.CharField(
        required=False,
        label="Buscar (DNI, Nombre, Apellidos, Email)",
        widget=forms.TextInput(attrs={"placeholder": "¿Qué cliente busca?"})
    )
        

        def clean(self):
            super().clean()

            textoBusqueda = self.cleaned_data.get("textoBusqueda")
            
            if not textoBusqueda:
                self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario.')
            
            if textoBusqueda and len(textoBusqueda) < 3:
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres.')

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
    

from django import forms
from .models import Socio, Cliente

class BusquedaSocioForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Texto de búsqueda")

    fecha_desde = forms.DateField(
        label="Fecha Desde",
        required=False,
        widget=forms.SelectDateWidget(years=range(2000, 2025))
    )

    fecha_hasta = forms.DateField(
        label="Fecha Hasta",
        required=False,
        widget=forms.SelectDateWidget(years=range(2000, 2025))
    )

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label="Cliente",
        empty_label="Selecciona un cliente",
    )

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get("textoBusqueda")
        fecha_desde = self.cleaned_data.get("fecha_desde")
        fecha_hasta = self.cleaned_data.get("fecha_hasta")
        cliente = self.cleaned_data.get("cliente")

        if not textoBusqueda and not cliente and not fecha_desde and not fecha_hasta:
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('cliente', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')

        if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
            self.add_error('fecha_desde', 'La fecha hasta no puede ser menor que la fecha desde')
            self.add_error('fecha_hasta', 'La fecha hasta no puede ser menor que la fecha desde')

        if textoBusqueda and len(textoBusqueda) < 3:
            self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres.')

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
        fechaLanzamiento = self.cleaned_data.get('fechaLanzamiento')

        #No puede haber dos películas con el mismo título
        peliculaTitulo = Pelicula.objects.filter(titulo=titulo).first()
        if(not peliculaTitulo is None):
            self.add_error('titulo','Ya existe una película con ese título')

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
            if textoBusqueda and len(textoBusqueda) < 3:
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres.')
            
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
        return self.cleaned_data
    
    
class empleadoModelForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['dni','nombre','apellidos','nuss','iban','salario','encargado','cine']
        labels = {
            "dni": ("DNI del empleado"),
        }
            
        def clean(self):
            super().clean()
            
            
            dni = self.cleaned_data.get('dni')
            nuss = self.cleaned_data.get('nuss')

            

            empleadoDni = Empleado.objects.filter(dni=dni).first()
            if(not empleadoDni is None
            ):
                if(not self.instance is None and empleadoDni.id == self.instance.id):
                    pass
                else:
                    self.add_error('dni','Ya existe un empleado con ese dni')


            if (len(nuss)<12 or len(nuss)>12):
                self.add_error('nuss','El NUSS debe tener 12 caracteres')


from django import forms
from .models import Empleado, Cine

class BusquedaEmpleadoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar (DNI, Nombre, Apellidos, NUSS, IBAN)")

    dni = forms.CharField(required=False)
    nombre = forms.CharField(required=False)
    apellidos = forms.CharField(required=False)
    nuss = forms.CharField(required=False)
    iban = forms.CharField(required=False)
    salario = forms.IntegerField(required=False, min_value=1100)
    cine = forms.ModelChoiceField(queryset=Cine.objects.all(), required=False, empty_label="Seleccione Cine")

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        dni = self.cleaned_data.get('dni')
        nombre = self.cleaned_data.get('nombre')
        apellidos = self.cleaned_data.get('apellidos')
        nuss = self.cleaned_data.get('nuss')
        iban = self.cleaned_data.get('iban')
        salario = self.cleaned_data.get('salario')
        cine = self.cleaned_data.get('cine')

        if (textoBusqueda == "" and not dni and not nombre and not apellidos and not nuss and not iban and not salario and not cine):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('dni', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('apellidos', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nuss', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('iban', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('salario', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('cine', 'Debe introducir al menos un valor en un campo del formulario')

        return self.cleaned_data



class cineModelForm(ModelForm):
    class Meta:
        model = Cine
        fields = ['direccion','telefono','email','gerente']
        labels = {
            "direccion": ("Dirección del cine"),
        }

    def clean(self):
            super().clean()
            
            
            direccion = self.cleaned_data.get('direccion')
            telefono = self.cleaned_data.get('telefono')
            email= self.cleaned_data.get('email')
            gerente = self.cleaned_data.get('gerente')

            cineDireccion = Cine.objects.filter(direccion=direccion).first()
            if(not cineDireccion is None
            ):
                if(not self.instance is None and cineDireccion.id == self.instance.id):
                    pass
                else:
                    self.add_error('direccion','Ya existe un cine en esa misma ubicación')


from django import forms

class BusquedaCineForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar (Dirección, Teléfono o Email)")
    direccion = forms.CharField(required=False)
    telefono = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    gerente = forms.CharField(required=False, label="Buscar por Gerente (Nombre o DNI)")

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        direccion = self.cleaned_data.get('direccion')
        telefono = self.cleaned_data.get('telefono')
        email = self.cleaned_data.get('email')
        gerente = self.cleaned_data.get('gerente')

        if (textoBusqueda == "" and not direccion and not telefono and not email and not gerente):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('email', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('gerente', 'Debe introducir al menos un valor en un campo del formulario')

        return self.cleaned_data


class gerenteModelForm(ModelForm):
    class Meta:
        model = Gerente
        fields = ['dni','nombre','apellidos','telefono']
        labels = {
            "dni": ("DNI del gerente"),
        }

        def clean(self):
            super().clean()
            
            
            dni = self.cleaned_data.get('dni')
            nombre = self.cleaned_data.get('nombre')
            apellidos= self.cleaned_data.get('apellidos')
            telefono = self.cleaned_data.get('telefono')

            gerenteDni = Gerente.objects.filter(dni=dni).first()
            if(not gerenteDni is None
            ):
                if(not self.instance is None and gerenteDni.id == self.instance.id):
                    pass
                else:
                    self.add_error('dni','Ya existe un/a gerente con ese DNI')

            if (len(telefono)<9 or len(telefono)>9):
                self.add_error('telefono','El teléfono debe tener 9 caracteres')


class BusquedaGerenteForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label='Texto de Búsqueda', 
                                    widget=forms.TextInput(attrs={'placeholder': 'DNI, nombre, apellidos o teléfono'}))
    
    dni = forms.CharField(required=False, label="DNI", widget=forms.TextInput(attrs={'placeholder': 'DNI'}))
    
    nombre = forms.CharField(required=False, label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    
    apellidos = forms.CharField(required=False, label="Apellidos", widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    
    telefono = forms.CharField(required=False, label="Teléfono", widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))

    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get("textoBusqueda")
        dni = self.cleaned_data.get("dni")
        nombre = self.cleaned_data.get("nombre")
        apellidos = self.cleaned_data.get("apellidos")
        telefono = self.cleaned_data.get("telefono")

        if (textoBusqueda == "" and not dni and not nombre and not apellidos and not telefono):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario.')
            self.add_error('dni', 'Debe introducir al menos un valor en un campo del formulario.')
            self.add_error('nombre', 'Debe introducir al menos un valor en un campo del formulario.')
            self.add_error('apellidos', 'Debe introducir al menos un valor en un campo del formulario.')
            self.add_error('telefono', 'Debe introducir al menos un valor en un campo del formulario.')

        return self.cleaned_data
    

#SESIONES Y PERMISOS

from django import forms
from django.forms import ModelForm
from .models import Entrada, Proyeccion

class EntradaForm(ModelForm):
    class Meta:
        model = Entrada
        fields = '__all__'
        widgets = {
            "cliente": forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(EntradaForm, self).__init__(*args, **kwargs)
        proyeccionesdisponibles = Proyeccion.objects.exclude(entradas_proyeccion__cliente=self.request.user.clientes_usuario).all()
        self.fields["proyeccion"] = forms.ModelChoiceField(
            queryset=proyeccionesdisponibles,
            widget=forms.Select,
            required=True,
            empty_label="Ninguna"
        )

class RegistroForm(UserCreationForm):
    roles = (
        (Usuario.CLIENTE, 'cliente'),
        (Usuario.EMPLEADO, 'empleado'),
        (Usuario.GERENTE, 'gerente'),
    )
    
    rol = forms.ChoiceField(choices=roles, widget=forms.Select(attrs={'class': 'field-rol'}))
    dni = forms.CharField(required=True, label="DNI", widget=forms.TextInput(attrs={'class': 'field-dni'}))
    cine = forms.ModelChoiceField(queryset=Cine.objects.all(), required=False, label="Cine (Rellene únicamente si es empleado)", widget=forms.Select(attrs={'class': 'field-cine'}))

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol', 'cine')

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        if rol == str(Usuario.EMPLEADO):
            if not cleaned_data.get('cine'):
                self.add_error('cine', 'Este campo es obligatorio para empleados.')
        return cleaned_data
    

class BusquedaEntradaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False, label="Buscar (Película, Sala, Fecha)")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['entradas'] = forms.ModelChoiceField(
                queryset=Entrada.objects.filter(cliente=user.cliente),
                required=False,
                label="Entradas"
            )

class BusquedaSalaForm(forms.Form):
    TAMANO_CHOICES = [
        ('PE', 'Pequeña'),
        ('ME', 'Mediana'),
        ('GR', 'Grande'),
    ]
    tamano = forms.ChoiceField(required=False, choices=TAMANO_CHOICES, label="Tamaño de la Sala")
    cine = forms.IntegerField(required=False, label="ID del Cine")