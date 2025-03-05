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
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny


@api_view(['GET'])
def cliente_list(request):
    if not request.user.has_perm('GestionCine.view_cliente'):
        return Response({"error": "No tienes permiso para ver clientes"}, status=status.HTTP_403_FORBIDDEN)
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def empleados_list(request):
    if not request.user.has_perm('GestionCine.view_empleado'):
        return Response({"error": "No tienes permiso para ver empleados"}, status=status.HTTP_403_FORBIDDEN)
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cine_list(request):
    if not request.user.has_perm('GestionCine.view_cine'):
        return Response({"error": "No tienes permiso para ver cines"}, status=status.HTTP_403_FORBIDDEN)
    cines = Cine.objects.all()
    serializer = CineSerializer(cines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sala_list(request):
    if not request.user.has_perm('GestionCine.view_sala'):
        return Response({"error": "No tienes permiso para ver salas"}, status=status.HTTP_403_FORBIDDEN)
    salas = Sala.objects.all().select_related("cine")
    serializer = SalaSerializer(salas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pelicula_list(request):
    if not request.user.has_perm('GestionCine.view_pelicula'):
        return Response({"error": "No tienes permiso para ver películas"}, status=status.HTTP_403_FORBIDDEN)
    peliculas = Pelicula.objects.all().prefetch_related("sala").all()
    serializer = PeliculaSerializerMejorado(peliculas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cliente_buscar(request):
    if not request.user.has_perm('GestionCine.view_cliente'):
        return Response({"error": "No tienes permiso para buscar clientes"}, status=status.HTTP_403_FORBIDDEN)
    formulario = BusquedaClienteForm(request.query_params)
    if formulario.is_valid():
        texto = formulario.data.get('textoBusqueda')
        clientes = Cliente.objects.filter(Q(nombre__icontains=texto) | Q(apellidos__icontains=texto)).all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cine_buscar(request):
    if not request.user.has_perm('GestionCine.view_cine'):
        return Response({"error": "No tienes permiso para buscar cines"}, status=status.HTTP_403_FORBIDDEN)
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
    if not request.user.has_perm('GestionCine.view_sala'):
        return Response({"error": "No tienes permiso para buscar salas"}, status=status.HTTP_403_FORBIDDEN)
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
    if not request.user.has_perm('GestionCine.view_pelicula'):
        return Response({"error": "No tienes permiso para buscar películas"}, status=status.HTTP_403_FORBIDDEN)
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


@api_view(['POST'])
def cliente_create(request):
    if not request.user.has_perm('GestionCine.add_cliente'):
        return Response({"error": "No tienes permiso para crear clientes"}, status=status.HTTP_403_FORBIDDEN)
    print(request.data)
    clienteCreateSerializer = ClienteSerializerCreate(data=request.data)
    if clienteCreateSerializer.is_valid():
        try:
            clienteCreateSerializer.save()
            return Response("Cliente creado", status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(clienteCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cliente_obtener(request, cliente_id):
    if not request.user.has_perm('GestionCine.view_cliente'):
        return Response({"error": "No tienes permiso para ver clientes"}, status=status.HTTP_403_FORBIDDEN)
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    except Cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def cliente_editar(request, cliente_id):
    if not request.user.has_perm('GestionCine.change_cliente'):
        return Response({"error": "No tienes permiso para editar clientes"}, status=status.HTTP_403_FORBIDDEN)
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClienteSerializer(cliente, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def cliente_actualizar_nombre(request, cliente_id):
    if not request.user.has_perm('GestionCine.change_cliente'):
        return Response({"error": "No tienes permiso para actualizar clientes"}, status=status.HTTP_403_FORBIDDEN)
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClienteSerializer(cliente, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"mensaje": "Nombre actualizado", "cliente": serializer.data})
        except Exception as error:
            print(repr(error))
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def cliente_eliminar(request, cliente_id):
    if not request.user.has_perm('GestionCine.delete_cliente'):
        return Response({"error": "No tienes permiso para eliminar clientes"}, status=status.HTTP_403_FORBIDDEN)
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.delete()
        return Response({"mensaje": "Cliente eliminado correctamente"}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def sala_create(request):
    if not request.user.has_perm('GestionCine.add_sala'):
        return Response({"error": "No tienes permiso para crear salas"}, status=status.HTTP_403_FORBIDDEN)
    serializer = SalaSerializerCreate(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def sala_obtener(request, sala_id):
    if not request.user.has_perm('GestionCine.view_sala'):
        return Response({"error": "No tienes permiso para ver salas"}, status=status.HTTP_403_FORBIDDEN)
    try:
        sala = Sala.objects.get(id=sala_id)
        serializer = SalaSerializer(sala)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sala.DoesNotExist:
        return Response({"error": "Sala no encontrada"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def sala_editar(request, sala_id):
    if not request.user.has_perm('GestionCine.change_sala'):
        return Response({"error": "No tienes permiso para editar salas"}, status=status.HTTP_403_FORBIDDEN)
    sala = Sala.objects.get(id=sala_id)
    sala_serializer = SalaSerializerEditar(data=request.data, instance=sala)
    if sala_serializer.is_valid():
        try:
            sala_serializer.save()
            return Response("Sala editada con éxito", status=status.HTTP_200_OK)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def sala_actualizar_tamano(request, sala_id):
    if not request.user.has_perm('GestionCine.change_sala'):
        return Response({"error": "No tienes permiso para actualizar salas"}, status=status.HTTP_403_FORBIDDEN)
    sala = Sala.objects.get(id=sala_id)
    sala_serializer = SalaSerializerActualizarTamano(data=request.data, instance=sala)
    if sala_serializer.is_valid():
        try:
            sala_serializer.save()
            return Response("Tamaño de la sala actualizado", status=status.HTTP_200_OK)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def sala_eliminar(request, sala_id):
    if not request.user.has_perm('GestionCine.delete_sala'):
        return Response({"error": "No tienes permiso para eliminar salas"}, status=status.HTTP_403_FORBIDDEN)
    sala = Sala.objects.get(id=sala_id)
    try:
        sala.delete()
        return Response("Sala eliminada con éxito", status=status.HTTP_200_OK)
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def pelicula_create(request):
    if not request.user.has_perm('GestionCine.add_pelicula'):
        return Response({"error": "No tienes permiso para crear películas"}, status=status.HTTP_403_FORBIDDEN)
    serializer = PeliculaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pelicula_obtener(request, pelicula_id):
    if not request.user.has_perm('GestionCine.view_pelicula'):
        return Response({"error": "No tienes permiso para ver películas"}, status=status.HTTP_403_FORBIDDEN)
    try:
        pelicula = Pelicula.objects.get(id=pelicula_id)
        serializer = PeliculaSerializer(pelicula)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pelicula.DoesNotExist:
        return Response({"error": "Pelicula no encontrada"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def pelicula_editar(request, pelicula_id):
    if not request.user.has_perm('GestionCine.change_pelicula'):
        return Response({"error": "No tienes permiso para editar películas"}, status=status.HTTP_403_FORBIDDEN)
    try:
        pelicula = Pelicula.objects.get(id=pelicula_id)
    except Pelicula.DoesNotExist:
        return Response({"error": "Pelicula no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PeliculaSerializer(pelicula, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def pelicula_actualizar_nombre(request, pelicula_id):
    if not request.user.has_perm('GestionCine.change_pelicula'):
        return Response({"error": "No tienes permiso para actualizar películas"}, status=status.HTTP_403_FORBIDDEN)
    try:
        pelicula = Pelicula.objects.get(id=pelicula_id)
    except Pelicula.DoesNotExist:
        return Response({"error": "Pelicula no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PeliculaSerializer(pelicula, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def pelicula_eliminar(request, pelicula_id):
    if not request.user.has_perm('GestionCine.delete_pelicula'):
        return Response({"error": "No tienes permiso para eliminar películas"}, status=status.HTTP_403_FORBIDDEN)
    try:
        pelicula = Pelicula.objects.get(id=pelicula_id)
        pelicula.delete()
        return Response({"mensaje": "Pelicula eliminada correctamente"}, status=status.HTTP_200_OK)
    except Pelicula.DoesNotExist:
        return Response({"error": "Pelicula no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]


class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"), 
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user)
                    cliente.save()
                elif(rol == Usuario.EMPLEADO):
                    grupo = Group.objects.get(name='Empleados') 
                    grupo.user_set.add(user)
                    empleado = Empleado.objects.create(usuario = user)
                    empleado.save()
                elif(rol == Usuario.GERENTE):
                    grupo = Group.objects.get(name='Gerentes') 
                    grupo.user_set.add(user)
                    gerente = Gerente.objects.create(usuario = user)
                    gerente.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


from oauth2_provider.models import AccessToken
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)