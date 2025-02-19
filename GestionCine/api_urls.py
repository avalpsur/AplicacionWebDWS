from django.urls import path

from  .api_views import *

urlpatterns = [
    path('clientes',cliente_list),
    path('cines',cine_list),
    path('salas',sala_list),
    path('peliculas',pelicula_list),
    path('empleados', empleados_list),
    
    path('clientes/buscar',cliente_buscar),
    path('cines/buscar',cine_buscar),
    path('salas/buscar',sala_buscar),
    path('peliculas/buscar',pelicula_buscar),
    
    path('clientes/<int:cliente_id>', cliente_obtener, name='cliente_obtener'),
    path('clientes/create', cliente_create, name='cliente_create'),
    path('clientes/<int:cliente_id>/editar', cliente_editar, name='cliente_editar'),
    path('clientes/<int:cliente_id>/actualizar/nombre', cliente_actualizar_nombre, name='cliente_actualizar_nombre'),
    path('clientes/<int:cliente_id>/eliminar', cliente_eliminar, name='cliente_eliminar'),

    path('salas/create',sala_create,name='sala_create'),
]
