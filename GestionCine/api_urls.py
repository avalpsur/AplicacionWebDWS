from django.urls import path

from .api_views import *

urlpatterns = [
    path('clientes', cliente_list),
    path('cines', cine_list),
    path('salas', sala_list),
    path('peliculas', pelicula_list),
    path('empleados', empleados_list),
    
    path('clientes/buscar', cliente_buscar),
    path('cines/buscar', cine_buscar),
    path('salas/buscar', sala_buscar),
    path('peliculas/buscar', pelicula_buscar),
    
    path('clientes/<int:cliente_id>', cliente_obtener, name='cliente_obtener'),
    path('clientes/create', cliente_create, name='cliente_create'),
    path('clientes/<int:cliente_id>/editar', cliente_editar, name='cliente_editar'),
    path('clientes/<int:cliente_id>/actualizar/nombre', cliente_actualizar_nombre, name='cliente_actualizar_nombre'),
    path('clientes/<int:cliente_id>/eliminar', cliente_eliminar, name='cliente_eliminar'),

    path('salas/create', sala_create, name='sala_create'),
    path('salas/<int:sala_id>/editar', sala_editar, name='sala_editar'),
    path('salas/<int:sala_id>/actualizar/tamano', sala_actualizar_tamano, name='sala_actualizar_tamano'),
    path('salas/<int:sala_id>/eliminar', sala_eliminar, name='sala_eliminar'),
    path('salas/<int:sala_id>', sala_obtener, name='sala_obtener'),

    path('peliculas/create', pelicula_create, name='pelicula_create'),
    path('peliculas/<int:pelicula_id>/editar', pelicula_editar, name='pelicula_editar'),
path('peliculas/<int:pelicula_id>/actualizar/nombre', pelicula_actualizar_nombre, name='pelicula_actualizar_nombre'),
path('peliculas/<int:pelicula_id>/eliminar', pelicula_eliminar, name='pelicula_eliminar'),
    path('peliculas/<int:pelicula_id>', pelicula_obtener, name='pelicula_obtener'),
]