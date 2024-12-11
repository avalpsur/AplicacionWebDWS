from django.shortcuts import render, redirect
from django.db.models import Q,Prefetch,Avg
from django.forms import modelform_factory
from datetime import timedelta
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

#Lista de socios
def listar_socios(request):
    socios = (Socio.objects.select_related("cliente")).all()
    return render(request, 'socio/lista.html',{"socios":socios})

#Lista de salas en un cine en concreto
def listar_salas_cine(request,id_cine):
    salas = (Sala.objects.select_related("cine").prefetch_related("empleado"))
    salas = salas.filter(cine=id_cine).all()
    return render(request, 'sala/lista.html',{"salas":salas})

#Lista de proyecciones de una sala ordenadas de manera ascendente
def listar_proyecciones(request,id_sala):
    proyecciones = Proyeccion.objects.select_related("sala","pelicula")
    proyecciones = proyecciones.filter(sala=id_sala).order_by("hora").all()
    return render(request,"proyeccion/lista.html",{"proyecciones":proyecciones})

#Lista de clientes que no son socios
def listar_clientes(request):
    clientes = Cliente.objects.filter(socios_cliente=None).all()
    return render(request,"cliente/lista.html",{"clientes":clientes})

#Última proyección de un cine en concreto
def listar_proyecciones_cine(request,id_cine):
    proyeccion = Proyeccion.objects.select_related("sala","pelicula")
    proyeccion = proyeccion.filter(sala__cine=id_cine).order_by("-hora")[0:1].get()
    return render(request,"proyeccion/proyeccion.html",{"proyeccion":proyeccion})

#Media salarial de los empleados
def media_salarios(request):
    media = Empleado.objects.aggregate(salario__avg=Avg("salario"))
    return render(request,"empleado/media.html",{"media":media})

#Lista de salas en las que se proyectarán películas cuya sinopsis empiece por un texto pasado como parámetro.
def listar_salas_sinopsis(request,texto):
    salas = (Sala.objects.select_related("cine").prefetch_related("empleado"))
    salas = salas.filter(peliculas_sala__sinopsis__startswith=texto).distinct()
    return render(request, 'sala/lista.html',{"salas":salas})

#Lista de películas de más de 3 horas que se proyecten en una sala en concreto
def listar_peliculas(request,id_sala):
    peliculas = Pelicula.objects.prefetch_related("sala")
    peliculas = peliculas.filter(
        tiempoProyectada__gte = timedelta(hours=3),
        sala = id_sala
    ).all()
    return render(request,'pelicula/lista.html',{'peliculas':peliculas})

#Se obtienen las salas de un cine pero esta vez de forma reversa
def mostrar_salasReversa(request,id_cine):
    cine = Cine.objects.prefetch_related(Prefetch("salas_cine")).get(id=id_cine)
    return render(request,'cine/cine.html',{"cine":cine})

#Lista de encargados o empleados con un sueldo de más de 1300 euros de un cine en concreto
def listar_encargados(request,id_cine):
    empleados = Empleado.objects.select_related("cine")
    empleados = empleados.filter(
        Q(encargado=True)|Q(salario__gt=1300),
        cine=id_cine
        ).all()
    return render(request,'empleado/lista.html',{"empleados":empleados})


def cliente_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = ClienteModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("lista_clientes")
            except Exception as error:
                print(error)
                
    return render(request, 'cliente/create.html',{"formulario":formulario})





def socio_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = SocioModelForm(datosFormulario)
    
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("lista_socios")
            except Exception as error:
                print(error)
                
    return render(request, 'socio/create.html',{"formulario":formulario})


def pelicula_create(formulario):
    pelicula_creada = False

    if formulario.is_valid():

        pelicula = Pelicula.objects.create(
            titulo = formulario.cleaned_data.get('titulo'),
            director = formulario.cleaned_data.get('director'),
            sinopsis = formulario.cleaned_data.get('sinopsis'),
            fechaLanzamiento = formulario.cleaned_data.get('fechaLanzamiento'),
            tiempoProyectada = formulario.cleaned_data.get('tiempoProyectada'),
        )
        pelicula.sala.set(formulario.cleaned_data.get('sala'))
        try:
            pelicula.save()
            pelicula_creada=True
        except:
            pass
    return pelicula_creada


def pelicula_buscar(request):

    if(len(request.GET) > 0):
        formulario = BusquedaPeliculaForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSpeliculas = Pelicula.objects.prefetch_related("sala")
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            sala = formulario.cleaned_data.get('sala')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            
            if(textoBusqueda != ""):
                QSpeliculas = QSpeliculas.filter(Q(titulo__icontains=textoBusqueda) | Q(director__icontains=textoBusqueda))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+textoBusqueda+"\n"
            
            if(len(sala) > 0):
                mensaje_busqueda +=" La sala sea "+sala[0]
                filtroOR = Q(sala=sala[0])
                for sala in sala[1:]:
                    mensaje_busqueda += " o "+sala[1]
                    filtroOR |= Q(sala=sala)
                mensaje_busqueda += "\n"
                QSpeliculas =  QSpeliculas.filter(filtroOR)
            
             
            if(not fechaDesde is None):
                mensaje_busqueda += " La fecha sea mayor a " + fechaDesde.strftime('%d-%m-%Y') + "\n"
                QSpeliculas = QSpeliculas.filter(fechaLanzamiento__gte=fechaDesde)
            
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+fechaHasta.strftime('%d-%m-%Y')+"\n"
                QSpeliculas = QSpeliculas.filter(fechaLanzamiento__lte=fechaHasta)
            
            peliculas = QSpeliculas.all()
    
            return render(request, 'pelicula/lista_busqueda.html',
                            {"peliculas_mostrar":peliculas,
                             "texto_busqueda":mensaje_busqueda})
    else:
       formulario = BusquedaPeliculaForm(None)
    return render(request, 'pelicula/busqueda_avanzada_datepicker.html',{"formulario":formulario})
  
def pelicula_editar(request, pelicula_id):
    pelicula = Pelicula.objects.get(id=pelicula_id)  # Obtenemos la película
    
    # Si el formulario es POST, procesamos los datos
    if request.method == "POST":
        formulario = PeliculaForm(request.POST)  # Crear el formulario con los datos POST
        
        if formulario.is_valid():
            # Si el formulario es válido, guardamos la película manualmente
            pelicula.titulo = formulario.cleaned_data['titulo']
            pelicula.director = formulario.cleaned_data['director']
            pelicula.sinopsis = formulario.cleaned_data['sinopsis']
            pelicula.fechaLanzamiento = formulario.cleaned_data['fechaLanzamiento']
            pelicula.tiempoProyectada = formulario.cleaned_data['tiempoProyectada']
            pelicula.save()  # Guardamos la instancia de la película
            
            messages.success(request, f'Se ha editado la película "{pelicula.titulo}" correctamente')
            return redirect('pelicula_lista')  # Redirigir a la lista de películas después de guardar
        
    else:
        # Si el método no es POST, mostramos el formulario con los datos actuales de la película
        formulario = PeliculaForm(initial={
            'titulo': pelicula.titulo,
            'director': pelicula.director,
            'sinopsis': pelicula.sinopsis,
            'fechaLanzamiento': pelicula.fechaLanzamiento,
            'tiempoProyectada': pelicula.tiempoProyectada,
        })
    
    return render(request, 'pelicula/actualizar.html', {"formulario": formulario, "pelicula": pelicula})


def pelicula_eliminar(request,pelicula_id):
    pelicula = Pelicula.objects.filter(id=pelicula_id).all()
    try:
        pelicula.delete()
        messages.success(request, "Se ha elimnado la pelicula "+pelicula.titulo+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_socios')

#Errores
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)