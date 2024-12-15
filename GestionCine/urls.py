from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('socios/listar',views.listar_socios,name='lista_socios'),
    path('salas/listar/<int:id_cine>',views.listar_salas_cine,name='lista_salas_cine'),
    path('proyecciones/listar/<int:id_sala>',views.listar_proyecciones,name='lista_proyecciones'),
    path('clientes/listar',views.listar_clientes,name='lista_clientes'),
    path('empleados/listar',views.listar_empleados,name='lista_empleados'),
    path('cines/listar',views.listar_cines,name='lista_cines'),
    path('gerentes/listar',views.listar_gerentes,name='lista_gerentes'),
    path('proyecciones_en_cine/<int:id_cine>',views.listar_proyecciones_cine,name='lista_proyecciones_cine'),
    path('media_salarios',views.media_salarios,name='media_salarios'),
    path('salas/listar_por_sinopsis/<str:texto>',views.listar_salas_sinopsis,name="lista_salas_sinopsis"),
    path('peliculas/listar/<int:id_sala>',views.listar_peliculas,name="lista_peliculas"),
    path('cine/mostrar_salasReversa/<int:id_cine>',views.mostrar_salasReversa,name="mostrar_salasReversa"),
    re_path(r"^filtro/(?P<id_cine>\d+)$",views.listar_encargados,name="lista_encargados"),
    
    path('cliente/create',views.cliente_create,name='cliente_create'),
    path('cliente/buscar',views.cliente_buscar,name='cliente_buscar'),
    path('cliente/editar/<int:cliente_id>',views.cliente_editar,name='cliente_editar'),
    path('cliente/eliminar/<int:cliente_id>',views.cliente_eliminar,name='cliente_eliminar'),


    path('socio/create',views.socio_create, name='socio_create'),
    path('socio/buscar',views.socio_buscar,name='socio_buscar'),
    path('socio/editar/<int:socio_id>',views.socio_editar,name='socio_editar'),
    path('socio/eliminar/<int:socio_id>',views.socio_eliminar,name='socio_eliminar'),


    path('pelicula/create',views.pelicula_create,name='pelicula_create'),
    path('pelicula/buscar',views.pelicula_buscar,name='pelicula_buscar'),
    path('pelicula/editar/<int:pelicula_id>',views.pelicula_editar,name='pelicula_editar'),
    path('pelicula/eliminar/<int:pelicula_id>',views.pelicula_eliminar,name='pelicula_eliminar'),
  
    path('empleado/create',views.empleado_create,name='empleado_create'),
    path('empleado/buscar',views.empleado_buscar,name='empleado_buscar'),
    path('empleado/editar/<int:empleado_id>',views.empleado_editar,name='empleado_editar'),
    path('empleado/eliminar/<int:empleado_id>',views.empleado_eliminar,name='empleado_eliminar'),


    path('cine/create',views.cine_create,name='cine_create'),
    path('cine/buscar',views.cine_buscar,name='cine_buscar'),
    path('cine/editar/<int:cine_id>',views.cine_editar,name='cine_editar'),
    path('cine/eliminar/<int:cine_id>',views.cine_eliminar,name='cine_eliminar'),

    path('gerente/create',views.gerente_create,name='gerente_create'),
    path('gerente/buscar',views.gerente_buscar,name='gerente_buscar'),
    path('gerente/editar/<int:gerente_id>',views.gerente_editar,name='gerente_editar'),
    path('gerente/eliminar/<int:gerente_id>',views.gerente_eliminar,name='gerente_eliminar'),

]

