from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    EMPLEADO = 3
    GERENTE = 4
    
    ROLES = (
        (CLIENTE,'cliente'),
        (EMPLEADO,'empleado'),
        (GERENTE,'gerente'),
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,default=2
    )
    

class Cliente(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=300)
    email = models.EmailField(default='nombre@ejemplo.com')
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="clientes_usuario", null=True)

class Socio(models.Model):
    numSocio = models.CharField(max_length=5, unique=True)
    fechaAlta = models.DateField(default=timezone.now)
    fechaCaducidad = models.DateField(default=timezone.now)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name="socios_cliente")

class Gerente(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=300)
    telefono = models.CharField(max_length=9)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE,related_name="gerentes_usuario", null=True)

class Cine(models.Model):
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(default='nombre@ejemplo.com')
    gerente = models.OneToOneField(Gerente, on_delete=models.CASCADE)

class Empleado(models.Model):
    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=300)
    nuss = models.CharField(max_length=12, unique=True)
    iban = models.CharField(max_length=24, unique=True)
    salario = models.IntegerField(default=1100)
    encargado = models.BooleanField(default=False)
    cine = models.ForeignKey(Cine, on_delete=models.CASCADE, related_name="empleados_cine")
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="empleados_usuario", null=True)

class Sala(models.Model):
    TAMANO = [
        ("PE", "Pequena"),
        ("ME", "Mediana"),
        ("GR", "Grande"),
    ]
    tamano = models.CharField(
        max_length=2,
        choices=TAMANO,
        default='ME',
    )
    cine = models.ForeignKey(Cine, on_delete=models.CASCADE,related_name="salas_cine")
    empleado = models.ManyToManyField(Empleado,related_name="salas_empleado")

class Pelicula(models.Model):
    titulo = models.CharField(max_length=500)
    director = models.CharField(max_length=300)
    sinopsis = models.TextField(null=True)
    fechaLanzamiento = models.DateField(default=timezone.now)
    tiempoProyectada = models.DurationField(null=True)
    sala = models.ManyToManyField(Sala,related_name="peliculas_sala")

class Proyeccion(models.Model):
    hora = models.DateTimeField(default=timezone.now)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="proyecciones_sala")
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name="proyecciones_pelicula")

class Entrada(models.Model):
    fechaCompra = models.DateTimeField(default=timezone.now)
    cliente = models.OneToOneField(Cliente, on_delete=models.DO_NOTHING,related_name="entradas_cliente")
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE,related_name="entradas_proyeccion")

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=9)
    web = models.URLField(null=True)

class Producto(models.Model):
    TIPO = [
        ("co", "comida"),
        ("be", "bebida"),
    ]
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(
        max_length=2,
        choices=TIPO,
        default='co',
    )
    fechaCaducidad = models.DateField(default=timezone.now)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,related_name="productos_proveedor")
    cliente = models.ManyToManyField(Cliente,related_name="productos_cliente")