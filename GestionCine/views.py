from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')


def listar_socios(request):
    socios = (Socio.objects.select_related("cliente")).all()
    return render(request, 'socio/lista.html',{"socios":socios})


def listar_salas_cine(request,id_cine):
    salas = (Sala.objects.select_related("cine").prefetch_related("")).all()