from django.shortcuts import render
from django.db.models import Q,Prefetch,Avg
from datetime import timedelta
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

#Lista de socios
def listar_socios(request):
    socios = (Socio.objects.select_related("cliente")).all()
    return render(request, 'socio/lista.html',{"socios":socios})

#Lista de salas en un cine en concreto
def listar_salas_cine(request,id_cine):
    salas = (Sala.objects.select_related("cine").prefetch_related("empleado"))
    salas = salas.filter(cine=id_cine).all()
    return render(request, 'sala/lista.html',{"salas":salas})

#Lista de proyecciones de una sala ordenadas de manera ascendente
def listar_proyecciones(request,id_sala):
    proyecciones = Proyeccion.objects.select_related("sala","pelicula")
    proyecciones = proyecciones.filter(sala=id_sala).order_by("hora").all()
    return render(request,"proyeccion/lista.html",{"proyecciones":proyecciones})

#Lista de clientes que no son socios
def listar_clientes(request):
    clientes = Cliente.objects.filter(socios_cliente=None).all()
    return render(request,"cliente/lista.html",{"clientes":clientes})

#Última proyección de un cine en concreto
def listar_proyecciones_cine(request,id_cine):
    proyeccion = Proyeccion.objects.select_related("sala","pelicula")
    proyeccion = proyeccion.filter(sala__cine=id_cine).order_by("-hora")[0:1].get()
    return render(request,"proyeccion/proyeccion.html",{"proyeccion":proyeccion})

#Media salarial de los empleados
def media_salarios(request):
    media = Empleado.objects.aggregate(salario__avg=Avg("salario"))
    return render(request,"empleado/media.html",{"media":media})

#Lista de salas en las que se proyectarán películas cuya sinopsis empiece por un texto pasado como parámetro.
def listar_salas_sinopsis(request,texto):
    salas = (Sala.objects.select_related("cine").prefetch_related("empleado"))
    salas = salas.filter(peliculas_sala__sinopsis__startswith=texto).distinct()
    return render(request, 'sala/lista.html',{"salas":salas})

#Lista de películas de más de 3 horas que se proyecten en una sala en concreto
def listar_peliculas(request,id_sala):
    peliculas = Pelicula.objects.prefetch_related("sala")
    peliculas = peliculas.filter(
        tiempoProyectada__gte = timedelta(hours=3),
        sala = id_sala
    ).all()
    return render(request,'pelicula/lista.html',{'peliculas':peliculas})

#Se obtienen las salas de un cine pero esta vez de forma reversa
def mostrar_salasReversa(request,id_cine):
    cine = Cine.objects.prefetch_related(Prefetch("salas_cine")).get(id=id_cine)
    return render(request,'cine/cine.html',{"cine":cine})

#Lista de encargados o empleados con un sueldo de más de 1300 euros de un cine en concreto
def listar_encargados(request,id_cine):
    empleados = Empleado.objects.select_related("cine")
    empleados = empleados.filter(
        Q(encargado=True)|Q(salario__gt=1300),
        cine=id_cine
        ).all()
    return render(request,'empleado/lista.html',{"empleados":empleados})

#Errores
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)