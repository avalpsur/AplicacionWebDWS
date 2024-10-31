from django.shortcuts import render
from django.db.models import Q,Prefetch
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')


def listar_socios(request):
    socios = (Socio.objects.select_related("cliente")).all()
    return render(request, 'socio/lista.html',{"socios":socios})


def listar_salas_cine(request,id_cine):
    salas = (Sala.objects.select_related("cine").prefetch_related("empleado"))
    salas = salas.filter(cine=id_cine).all()
    return render(request, 'sala/lista.html',{"salas":salas})


def listar_proyecciones(request,id_sala):
    proyecciones = Proyeccion.objects.select_related("sala","pelicula")
    proyecciones = proyecciones.filter(sala=id_sala).order_by("hora").all()
    return render(request,"proyeccion/lista.html",{"proyecciones":proyecciones})