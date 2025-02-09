from django.urls import path

from  .api_views import *

urlpatterns = [
    path('clientes',cliente_list),
    path('cines',cine_list),
    path('salas',sala_list),
    path('peliculas',pelicula_list),
    
    path('clientes/buscar',cliente_buscar),
    path('cines/buscar',cine_buscar),
    path('salas/buscar',sala_buscar),
    path('peliculas/buscar',pelicula_buscar),
]