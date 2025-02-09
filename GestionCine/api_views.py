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
from django.shortcuts import render,redirect


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
    salas = Sala.objects.all().select_related("cine")
    serializer = SalaSerializer(salas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pelicula_list(request):
    peliculas = Pelicula.objects.all().prefetch_related("sala").all()
    serializer = PeliculaSerializerMejorado(peliculas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cliente_buscar(request):
    formulario = BusquedaClienteForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        clientes = Cliente.objects.filter(Q(nombre__icontains=texto) | Q(apellidos__icontains=texto)).all()
        serializer = ClienteSerializer(clientes,many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def cine_buscar(request):
    formulario = BusquedaCineForm(request.query_params)

    if formulario.is_valid():
        filtros = Q()  

        if formulario.cleaned_data.get('direccion'):
            filtros = Q(direccion__icontains=formulario.cleaned_data['direccion'])

        if formulario.cleaned_data.get('telefono'):
            filtros = Q(telefono__icontains=formulario.cleaned_data['telefono'])

        if formulario.cleaned_data.get('email'):
            filtros = Q(email__icontains=formulario.cleaned_data['email'])

        if filtros:
            cines = Cine.objects.filter(filtros).select_related("gerente")
        else:
            cines = Cine.objects.all()

        serializer = CineSerializer(cines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def sala_buscar(request):
    if len(request.query_params) > 0:
        tamano = request.query_params.get('tamano', None)
        cine_id = request.query_params.get('cine', None)
        
        QSsalas = Sala.objects.select_related('cine')
        
        if tamano:
            QSsalas = QSsalas.filter(tamano=tamano)
        if cine_id:
            QSsalas = QSsalas.filter(cine__id=cine_id)
        
        serializer = SalaSerializer(QSsalas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"error": "No se proporcionaron parámetros de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pelicula_buscar(request):
    if len(request.query_params) > 0:
        titulo = request.query_params.get('titulo', None)
        director = request.query_params.get('director', None)
        fecha_desde = request.query_params.get('fecha_desde', None)
        fecha_hasta = request.query_params.get('fecha_hasta', None)
        
        QSpeliculas = Pelicula.objects.all()
        
        if titulo:
            QSpeliculas = QSpeliculas.filter(titulo__icontains=titulo)
        if director:
            QSpeliculas = QSpeliculas.filter(director__icontains=director)
        if fecha_desde and fecha_hasta:
            QSpeliculas = QSpeliculas.filter(fechaLanzamiento__range=[fecha_desde, fecha_hasta])
        
        serializer = PeliculaSerializer(QSpeliculas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"error": "No se proporcionaron parámetros de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)