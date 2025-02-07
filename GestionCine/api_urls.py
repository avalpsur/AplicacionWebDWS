from django.urls import path

from  .api_views import *

urlpatterns = [
    path('clientes',cliente_list),
    path('cines',cine_list),
    path('salas',sala_list),
    path('peliculas',pelicula_list),
    
    path('clientes/buscar',cliente_buscar),
]