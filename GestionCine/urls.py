from django.urls import path,re_path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('socios/listar',views.listar_socios,name='lista_socios'),
]