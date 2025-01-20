from django.shortcuts import render, redirect
from django.db.models import Q,Prefetch,Avg
from django.forms import modelform_factory
from datetime import timedelta
from datetime import datetime
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group

# Create your views here.
def index(request):
    if not "fecha_inicio" in request.session:
        request.session["fecha_inicio"] = timezone.now().strftime('%d/%m/%Y %H:%M')
        request.session['variable1'] ='Cines Polígono Sur'
        request.session['variable2'] = '2025'
        request.session['variable3'] = 'C/ Esclava del Señor, 1'
        request.session['variable4'] = '41013'
    return render(request, 'index.html')


#Lista de socios
def listar_socios(request):
    socios = (Socio.objects.select_related("cliente")).all()
    return render(request, 'socio/lista.html',{"socios":socios})

def listar_empleados(request):
    empleados = (Empleado.objects.select_related("cine")).all()
    return render(request, 'empleado/lista.html',{"empleados":empleados})

def listar_cines(request):
    cines = (Cine.objects.select_related("gerente")).all()
    return render(request, 'cine/lista.html',{"cines":cines})

def listar_gerentes(request):
    gerentes = Gerente.objects.all()
    return render(request, 'gerente/lista.html',{"gerentes":gerentes})

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


#CRUD de Cliente
@permission_required('GestionCine.add_cliente')
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

def cliente_buscar(request):
    formulario = BusquedaClienteForm(request.GET or None)

    if formulario.is_valid():
        textoBusqueda = formulario.cleaned_data.get('textoBusqueda')

        qs_clientes = Cliente.objects.all()

        if textoBusqueda:
            qs_clientes = qs_clientes.filter(
                Q(dni__icontains=textoBusqueda) |
                Q(nombre__icontains=textoBusqueda) |
                Q(apellidos__icontains=textoBusqueda) |
                Q(email__icontains=textoBusqueda)
            )

        return render(request, 'cliente/lista_busqueda.html', {
            'clientes': qs_clientes,
            'formulario': formulario,
            'texto_busqueda': textoBusqueda,
        })

    return render(request, 'cliente/busqueda_avanzada.html', {'formulario': formulario})

@permission_required('GestionCine.change_cliente')
def cliente_editar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)  

    if request.method == "POST":
        formulario = ClienteModelForm(request.POST)  

        if formulario.is_valid():
            cliente.dni = formulario.cleaned_data['dni']
            cliente.nombre = formulario.cleaned_data['nombre']
            cliente.apellidos = formulario.cleaned_data['apellidos']
            cliente.email = formulario.cleaned_data['email']
            cliente.save() 

            messages.success(request, f'Se ha editado el cliente "{cliente.nombre} {cliente.apellidos}" correctamente.')
            return redirect('cliente_lista')  

    else:
        formulario = ClienteModelForm(initial={
            'dni': cliente.dni,
            'nombre': cliente.nombre,
            'apellidos': cliente.apellidos,
            'email': cliente.email,
        })

    return render(request, 'cliente/actualizar.html', {'formulario': formulario, 'cliente': cliente})

@permission_required('GestionCine.delete_cliente')
def cliente_eliminar(request,cliente_id):
    cliente = Cliente.objects.filter(id=cliente_id).all()
    try:
        cliente.delete()
        messages.success(request, "Se ha elimnado el cliente con DNI: "+cliente.dni+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_clientes')

#CRUD de Socio
@permission_required('GestionCine.add_socio')
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

def socio_buscar(request):
    if request.GET:
        formulario = BusquedaSocioForm(request.GET)
        if formulario.is_valid():
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')
            cliente = formulario.cleaned_data.get('cliente')

            qs_socios = Socio.objects.all()

            if textoBusqueda:
                qs_socios = qs_socios.filter(
                    Q(numSocio__icontains=textoBusqueda) |
                    Q(cliente__nombre__icontains=textoBusqueda) |
                    Q(cliente__apellidos__icontains=textoBusqueda)
                )

            if fecha_desde:
                qs_socios = qs_socios.filter(fechaAlta__gte=fecha_desde)

            if fecha_hasta:
                qs_socios = qs_socios.filter(fechaCaducidad__lte=fecha_hasta)

            if cliente:
                qs_socios = qs_socios.filter(cliente=cliente)

            return render(request, 'socio/lista_busqueda.html', {
                'socios': qs_socios,
                'formulario': formulario
            })
    else:
        formulario = BusquedaSocioForm()

    return render(request, 'socio/busqueda_avanzada_datepicker.html', {'formulario': formulario})
@login_required
@permission_required('GestionCine.change_socio')
def socio_editar(request, socio_id):
    socio = Socio.objects.get(id=socio_id) 

    if request.method == "POST":
        formulario = SocioModelForm(request.POST) 

        if formulario.is_valid():
            socio.numSocio = formulario.cleaned_data['numSocio']
            socio.fechaAlta = formulario.cleaned_data['fechaAlta']
            socio.fechaCaducidad = formulario.cleaned_data['fechaCaducidad']
            socio.save()

            messages.success(request, f'Se ha editado el socio "{socio.numSocio}" correctamente.')
            return redirect('socio_lista')

    else:
        formulario = SocioModelForm(initial={
            'numSocio': socio.numSocio,
            'fechaAlta': socio.fechaAlta,
            'fechaCaducidad': socio.fechaCaducidad,
        })

    return render(request, 'socio/actualizar.html', {'formulario': formulario, 'socio': socio})

@permission_required('GestionCine.delete_socio')
def socio_eliminar(request,socio_id):
    socio = Socio.objects.filter(id=socio_id).all()
    try:
        socio.delete()
        messages.success(request, "Se ha elimnado el socio: "+socio.numSocio+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_socios')


#CRUD de Película
@permission_required('GestionCine.add_pelicula')
def pelicula_create(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        
        if form.is_valid():
            try:
                pelicula = Pelicula.objects.create(
                    titulo=form.cleaned_data.get('titulo'),
                    director=form.cleaned_data.get('director'),
                    sinopsis=form.cleaned_data.get('sinopsis'),
                    fechaLanzamiento=form.cleaned_data.get('fechaLanzamiento'),
                    tiempoProyectada=form.cleaned_data.get('tiempoProyectada'),
                )
                
                pelicula.sala.set(form.cleaned_data.get('sala'))
                pelicula.save()  # Guardar la película

                return redirect('lista_peliculas')
            except Exception as e:
                form.add_error(None, f"Hubo un error al guardar la película: {e}")
        else:
            form.add_error(None, "Formulario inválido.")
    
    else:
        form = PeliculaForm() 
    
    return render(request, 'pelicula/create.html', {'form': form})


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
  

@permission_required('GestionCine.change_pelicula')
def pelicula_editar(request, pelicula_id):
    pelicula = Pelicula.objects.get(id=pelicula_id)  
    
    if request.method == "POST":
        formulario = PeliculaForm(request.POST)  
        
        if formulario.is_valid():
            
            pelicula.titulo = formulario.cleaned_data['titulo']
            pelicula.director = formulario.cleaned_data['director']
            pelicula.sinopsis = formulario.cleaned_data['sinopsis']
            pelicula.fechaLanzamiento = formulario.cleaned_data['fechaLanzamiento']
            pelicula.tiempoProyectada = formulario.cleaned_data['tiempoProyectada']
            pelicula.save()  
            
            messages.success(request, f'Se ha editado la película "{pelicula.titulo}" correctamente')
            return redirect('pelicula_lista')  
        
    else:

        formulario = PeliculaForm(initial={
            'titulo': pelicula.titulo,
            'director': pelicula.director,
            'sinopsis': pelicula.sinopsis,
            'fechaLanzamiento': pelicula.fechaLanzamiento,
            'tiempoProyectada': pelicula.tiempoProyectada,
        })
    
    return render(request, 'pelicula/actualizar.html', {"formulario": formulario, "pelicula": pelicula})

@permission_required('GestionCine.delete_pelicula')
def pelicula_eliminar(request,pelicula_id):
    pelicula = Pelicula.objects.filter(id=pelicula_id).all()
    try:
        pelicula.delete()
        messages.success(request, "Se ha elimnado la pelicula "+pelicula.titulo+" correctamente")
    except Exception as error:
        print(error)
    return redirect('index')

#CRUD de Empleado
@permission_required('GestionCine.add_empleado')
def empleado_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = empleadoModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("lista_empleados")
            except Exception as error:
                print(error)
                
    return render(request, 'empleado/create.html',{"formulario":formulario})

from django.shortcuts import render
from django.db.models import Q
from .forms import BusquedaEmpleadoForm
from .models import Empleado

def empleado_buscar(request):
    if request.method == 'GET':
        formulario = BusquedaEmpleadoForm(request.GET)
        
        if formulario.is_valid():
            empleados = Empleado.objects.all()

            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            dni = formulario.cleaned_data.get('dni')
            nombre = formulario.cleaned_data.get('nombre')
            apellidos = formulario.cleaned_data.get('apellidos')
            nuss = formulario.cleaned_data.get('nuss')
            iban = formulario.cleaned_data.get('iban')
            salario = formulario.cleaned_data.get('salario')
            cine = formulario.cleaned_data.get('cine')

            if textoBusqueda:
                empleados = empleados.filter(
                    Q(dni__icontains=textoBusqueda) |
                    Q(nombre__icontains=textoBusqueda) |
                    Q(apellidos__icontains=textoBusqueda) |
                    Q(nuss__icontains=textoBusqueda) |
                    Q(iban__icontains=textoBusqueda)
                )

            if dni:
                empleados = empleados.filter(dni__icontains=dni)

            if nombre:
                empleados = empleados.filter(nombre__icontains=nombre)

            if apellidos:
                empleados = empleados.filter(apellidos__icontains=apellidos)

            if nuss:
                empleados = empleados.filter(nuss__icontains=nuss)

            if iban:
                empleados = empleados.filter(iban__icontains=iban)

            if salario:
                empleados = empleados.filter(salario=salario)

            if cine:
                empleados = empleados.filter(cine=cine)

            if empleados.exists():
                return render(request, 'empleado/lista_busqueda.html', {'empleados': empleados})

            return render(request, 'empleado/lista_busqueda.html', {'mensaje': 'No se encontraron resultados.'})

        else:
            return render(request, 'empleado/busqueda_avanzada.html', {'formulario': formulario})

    else:
        formulario = BusquedaEmpleadoForm()
        return render(request, 'empleado/busqueda_avanzada.html', {'formulario': formulario})

# CRUD de Empleado
@permission_required('GestionCine.add_empleado')
def empleado_create(request):
    if request.method == "POST":
        formulario = empleadoModelForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Empleado creado correctamente")
                return redirect('lista_empleados')
            except Exception as error:
                messages.error(request, f"Error al crear empleado: {error}")
    else:
        formulario = empleadoModelForm()
    return render(request, 'empleado/create.html', {"formulario": formulario})

@permission_required('GestionCine.change_empleado')
def empleado_editar(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    if request.method == "POST":
        formulario = empleadoModelForm(request.POST, instance=empleado)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Empleado editado correctamente")
                return redirect('lista_empleados')
            except Exception as error:
                messages.error(request, f"Error al editar empleado: {error}")
    else:
        formulario = empleadoModelForm(instance=empleado)
    return render(request, 'empleado/actualizar.html', {'formulario': formulario, 'empleado': empleado})

@permission_required('GestionCine.delete_empleado')
def empleado_eliminar(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    try:
        empleado.delete()
        messages.success(request, "Empleado eliminado correctamente")
    except Exception as error:
        messages.error(request, f"Error al eliminar empleado: {error}")
    return redirect('lista_empleados')


#CRUD de Cine
@permission_required('GestionCine.add_cine')
def cine_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = cineModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("lista_cines")
            except Exception as error:
                print(error)
                
    return render(request, 'cine/create.html',{"formulario":formulario})


from django.shortcuts import render
from .models import Cine
from .forms import BusquedaCineForm
from django.db.models import Q

def cine_buscar(request):
    if request.method == 'GET':
        formulario = BusquedaCineForm(request.GET)
        
        if formulario.is_valid():
            cines = Cine.objects.all()

            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            direccion = formulario.cleaned_data.get('direccion')
            telefono = formulario.cleaned_data.get('telefono')
            email = formulario.cleaned_data.get('email')
            gerente = formulario.cleaned_data.get('gerente')

            if textoBusqueda:
                cines = cines.filter(
                    Q(direccion__icontains=textoBusqueda) |
                    Q(telefono__icontains=textoBusqueda) |
                    Q(email__icontains=textoBusqueda)
                )

            if direccion:
                cines = cines.filter(direccion__icontains=direccion)

            if telefono:
                cines = cines.filter(telefono__icontains=telefono)

            if email:
                cines = cines.filter(email__icontains=email)

            if gerente:
                cines = cines.filter(gerente__nombre__icontains=gerente) | \
                        cines.filter(gerente__dni__icontains=gerente)

            if cines.exists():
                return render(request, 'cine/lista_busqueda.html', {'cines': cines})

            return render(request, 'cine/lista_busqueda.html', {'mensaje': 'No se encontraron resultados.'})

        else:
            return render(request, 'cine/busqueda_avanzada.html', {'formulario': formulario})

    else:
        formulario = BusquedaCineForm()
        return render(request, 'cine/busqueda_avanzada.html', {'formulario': formulario})

@permission_required('GestionCine.change_cine')
def cine_editar(request, cine_id):
    cine = Cine.objects.get(id=cine_id)

    if request.method == "POST":
        formulario = cineModelForm(request.POST) 

        if formulario.is_valid():
            cine.direccion = formulario.cleaned_data['direccion']
            cine.telefono = formulario.cleaned_data['telefono']
            cine.email = formulario.cleaned_data['email']
            cine.gerente = formulario.cleaned_data['gerente']
            cine.save() 

            messages.success(request, f'Se ha editado el cine en la dirección "{cine.direccion}" correctamente.')
            return redirect('cine_lista')

    else:
        formulario = cineModelForm(initial={
            'direccion': cine.direccion,
            'telefono': cine.telefono,
            'email': cine.email,
            'gerente': cine.gerente,
        })

    return render(request, 'cine/actualizar.html', {'formulario': formulario, 'cine': cine})

@permission_required('GestionCine.delete_cine')
def cine_eliminar(request,cine_id):
    cine = Cine.objects.filter(id=cine_id).all()
    try:
        cine.delete()
        messages.success(request, "Se ha elimnado el cine con dirección: "+cine.direccion+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_cines')


#CRUD de Gerente

def gerente_buscar(request):
    if request.method == 'GET':
        formulario = BusquedaGerenteForm(request.GET)
        
        if formulario.is_valid():
            gerentes = Gerente.objects.all()

            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            dni = formulario.cleaned_data.get('dni')
            nombre = formulario.cleaned_data.get('nombre')
            apellidos = formulario.cleaned_data.get('apellidos')
            telefono = formulario.cleaned_data.get('telefono')

            if textoBusqueda:
                gerentes = gerentes.filter(
                    Q(dni__icontains=textoBusqueda) |
                    Q(nombre__icontains=textoBusqueda) |
                    Q(apellidos__icontains=textoBusqueda) |
                    Q(telefono__icontains=textoBusqueda)
                )

            if dni:
                gerentes = gerentes.filter(dni__icontains=dni)

            if nombre:
                gerentes = gerentes.filter(nombre__icontains=nombre)

            if apellidos:
                gerentes = gerentes.filter(apellidos__icontains=apellidos)

            if telefono:
                gerentes = gerentes.filter(telefono__icontains=telefono)

            return render(request, 'gerente/busqueda_avanzada.html', {'formulario': formulario, 'gerentes': gerentes})

        else:
            return render(request, 'gerente/busqueda_avanzada.html', {'formulario': formulario})
    
    else:
        formulario = BusquedaGerenteForm()
        return render(request, 'gerente/busqueda_avanzada.html', {'formulario': formulario})
@permission_required('GestionCine.add_gerente')
def gerente_create(request):
    if request.method == "POST":
        formulario = gerenteModelForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Gerente creado correctamente")
                return redirect('lista_gerentes')
            except Exception as error:
                messages.error(request, f"Error al crear gerente: {error}")
    else:
        formulario = gerenteModelForm()
    return render(request, 'gerente/create.html', {"formulario": formulario})

@permission_required('GestionCine.change_gerente')
def gerente_editar(request, gerente_id):
    gerente = Gerente.objects.get(id=gerente_id)
    if request.method == "POST":
        formulario = gerenteModelForm(request.POST, instance=gerente)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Gerente editado correctamente")
                return redirect('lista_gerentes')
            except Exception as error:
                messages.error(request, f"Error al editar gerente: {error}")
    else:
        formulario = gerenteModelForm(instance=gerente)
    return render(request, 'gerente/actualizar.html', {'formulario': formulario, 'gerente': gerente})

@permission_required('GestionCine.delete_gerente')
def gerente_eliminar(request, gerente_id):
    gerente = Gerente.objects.get(id=gerente_id)
    try:
        gerente.delete()
        messages.success(request, "Gerente eliminado correctamente")
    except Exception as error:
        messages.error(request, f"Error al eliminar gerente: {error}")
    return redirect('lista_gerentes')

#Sesiones y permisos
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if rol == Usuario.CLIENTE:
                grupo = Group.objects.get(name='Clientes')
                grupo.user_set.add(user)
                Cliente.objects.create(usuario=user)
            elif rol == Usuario.EMPLEADO:
                grupo = Group.objects.get(name='Empleados')
                grupo.user_set.add(user)
                Empleado.objects.create(usuario=user, cine=formulario.cleaned_data.get('cine'))
            elif rol == Usuario.GERENTE:
                grupo = Group.objects.get(name='Gerentes')
                grupo.user_set.add(user)
                Gerente.objects.create(usuario=user)
            
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

@login_required
@permission_required('GestionCine.add_entrada')
def entrada_crear(request):
    try:
        cliente = request.user.clientes_usuario
    except Cliente.DoesNotExist:
        messages.error(request, "El usuario no tiene un cliente asociado.")
        return redirect('index')

    if request.method == 'POST':
        formulario = EntradaForm(request.POST, request=request)
        if formulario.is_valid():
            entrada = formulario.save(commit=False)
            entrada.cliente = cliente
            entrada.save()
            return redirect("entrada_lista_usuario", usuario_id=cliente.id)
    else:
        formulario = EntradaForm(initial={"cliente": cliente}, request=request)
    return render(request, 'entrada/create.html', {'formulario': formulario})
@login_required
def buscar_entrada(request):
    if not hasattr(request.user, 'cliente'):
        messages.error(request, "El usuario no tiene un cliente asociado.")
        return redirect('index')

    if request.method == 'GET':
        formulario = BusquedaEntradaForm(request.GET, user=request.user)
        if formulario.is_valid():
            texto_busqueda = formulario.cleaned_data.get('textoBusqueda')
            entradas = Entrada.objects.filter(cliente=request.user.cliente)
            if texto_busqueda:
                entradas = entradas.filter(
                    Q(proyeccion__pelicula__titulo__icontains=texto_busqueda) |
                    Q(proyeccion__sala__nombre__icontains=texto_busqueda) |
                    Q(fechaCompra__icontains=texto_busqueda)
                )
            return render(request, 'entrada/lista_busqueda.html', {'entradas': entradas, 'formulario': formulario})
    else:
        formulario = BusquedaEntradaForm(user=request.user)
    return render(request, 'entrada/busqueda_avanzada.html', {'formulario': formulario})

@login_required
def entrada_lista_usuario(request, usuario_id):
    entradas = Entrada.objects.filter(cliente__usuario_id=usuario_id)
    return render(request, 'entrada/lista_usuario.html', {'entradas': entradas})
#Errores
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)