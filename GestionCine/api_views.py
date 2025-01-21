from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def cliente_list(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cine_list(request):
    cines = Cine.objects.all()
    serializer = CineSerializer(cines,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sala_list(request):
    salas = Sala.objects.all()
    serializer = SalaSerializer(salas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pelicula_list(request):
    peliculas = Pelicula.objects.all().prefetch_related("sala").all()
    serializer = PeliculaSerializer(peliculas,many=True)
    return Response(serializer.data)