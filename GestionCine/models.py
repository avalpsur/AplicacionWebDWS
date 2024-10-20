from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Cliente(models.Model):
    dni = models.CharField(max_length=9,unique=True)
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=300)
    correoElectronico = models.EmailField

class Socio(models.Model):
    numSocio = models.CharField(max_length=5,unique = True)
    fechaAlta = models.DateField
    fechaCaducidad = models.DateField
    cliente = models.OneToOneField(Cliente,on_delete=models.CASCADE)

class Gerente(models.Model):
    dni = models.CharField(max_length=9,unique=True)
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=300)
    telefono = models.CharField(max_length=9)

class Cine(models.Model):
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=9)
    email = models.EmailField

    gerente = models.OneToOneField(Gerente,on_delete=models.CASCADE)


class Empleado(models.Model):
    dni = models.CharField(max_length=9,unique=True)
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=300)
    nuss = models.CharField(max_length=12,unique=True)
    iban = models.CharField(max_length=24,unique=True)
    salario = models.IntegerField
    encargado = models.BooleanField(default=False)
    
    cine = models.ForeignKey(Cine,on_delete = models.CASCADE)



class Sala(models.Model):
    TAMANO = [
        ("PE","Pequena"),
        ("ME","Mediana"),
        ("GR","Grande"),
    ]


    tamano = models.CharField(
        max_length=2,
        choices=TAMANO,
        default='ME',
    )

    cine = models.ForeignKey(Cine,on_delete = models.CASCADE)
    empleado = models.ManyToManyField(Empleado)


class Pelicula(models.Model):
    titulo = models.CharField(max_length=500)
    director = models.CharField(max_length=300)
    sinopsis = models.TextField
    fechaLanzamiento = models.DateField
    tiempoProyectada = models.DurationField
    sala = models.ManyToManyField(Sala)


class Proyeccion(models.Model):
    hora = models.DateTimeField
    sala = models.ForeignKey(Sala,on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    


class Entrada(models.Model):
    fechaCompra = models.DateTimeField
    cliente = models.OneToOneField(Cliente,on_delete=models.DO_NOTHING)
    proyeccion = models.ForeignKey(Proyeccion,on_delete=models.CASCADE)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=9)
    web = models.URLField


class Producto(models.Model):
    TIPO = [
        ("co","comida"),
        ("be","bebida"),
    ]
    
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(
        max_length=2,
        choices = TIPO,
        default = 'co',
    )
    fechaCaducidad = models.DateField
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    cliente = models.ManyToManyField(Cliente)