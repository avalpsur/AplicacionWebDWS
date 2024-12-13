from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('socios/listar',views.listar_socios,name='lista_socios'),
    path('salas/listar/<int:id_cine>',views.listar_salas_cine,name='lista_salas_cine'),
    path('proyecciones/listar/<int:id_sala>',views.listar_proyecciones,name='lista_proyecciones'),
    path('clientes/listar',views.listar_clientes,name='lista_clientes'),
    path('proyecciones_en_cine/<int:id_cine>',views.listar_proyecciones_cine,name='lista_proyecciones_cine'),
    path('media_salarios',views.media_salarios,name='media_salarios'),
    path('salas/listar_por_sinopsis/<str:texto>',views.listar_salas_sinopsis,name="lista_salas_sinopsis"),
    path('peliculas/listar/<int:id_sala>',views.listar_peliculas,name="lista_peliculas"),
    path('cine/mostrar_salasReversa/<int:id_cine>',views.mostrar_salasReversa,name="mostrar_salasReversa"),
    re_path(r"^filtro/(?P<id_cine>\d+)$",views.listar_encargados,name="lista_encargados"),
    
    path('cliente/create',views.cliente_create,name='cliente_create'),
    #path('cliente/buscar',views.cliente_buscar,name='cliente_buscar'),

    path('socio/create',views.socio_create, name='socio_create'),

    path('pelicula/create',views.pelicula_create,name='pelicula_create'),
    path('pelicula/buscar',views.pelicula_buscar,name='pelicula_buscar'),
    path('pelicula/editar/<int:pelicula_id>',views.pelicula_editar,name='pelicula_editar'),
    path('pelicula/eliminar/<int:pelicula_id>',views.pelicula_eliminar,name='pelicula_eliminar'),

    path('gerente/create',views.gerente_create,name='gerente_create'),
    
]

