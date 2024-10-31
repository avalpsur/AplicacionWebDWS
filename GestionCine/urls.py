from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('socios/listar',views.listar_socios,name='lista_socios'),
    path('salas/listar/<int:id_cine>',views.listar_salas_cine,name='lista_salas_cine'),
]