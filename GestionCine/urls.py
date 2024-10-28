from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',view.index,name='index'),
    path('clientes/listar',views.listar_clientes,name='lista_clientes'),
]