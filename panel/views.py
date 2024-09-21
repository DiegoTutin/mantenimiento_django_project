from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Clientes, Tipo_equipos, Ordenes_Mantenimiento, Accesorio, Estado, MisOrdenes
from django.utils import timezone
#paginacion 
from django.core.paginator import Paginator


# Clase para crear login por defecto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


#Barra de busqueda

from django.db.models import Q

#Buscar clientes
from django.http import JsonResponse
from django.forms.models import model_to_dict

#generar pdf
from django.template.loader import get_template
from xhtml2pdf import pisa



TEMPLATE_DIRS = 'os.path.join(BASE_DIR, "templates")'


def registroUsuarios(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": UserCreationForm()})
    elif request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    first_name = request.POST["first_name"],
                    last_name = request.POST["last_name"],
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    email=request.POST["email"],
                )
                user.save()
                login(request, user)
                return redirect("index")
            except IntegrityError as e:
                if "UNIQUE constraint" in str(e):
                    messages.error(request, "El usuario ya existe")
                else:
                    messages.error(request, "Error al crear el usuario")
        else:
            messages.error(request, "Las contraseñas no coinciden")
        return redirect("registro")


def cerrarSesion(request):
    logout(request)
    return redirect("login")


def inicioSesion(request):
    if request.method == 'GET':
        return render(request, "inicio_sesion.html", 
                      {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password'] )

        if user is None:
            return render (request, "inicio_sesion.html", {
                "form": AuthenticationForm(),
                "error" : "Usuario no encontrado"
            })
        else:
            login(request, user)
            return redirect('index')

@login_required(login_url = 'login')
def index(request):
    return render(request, "index.html")


def dashboard(request):
    cantidad_clientes = Clientes.objects.count()
    cantidad_tipos_equipos = Tipo_equipos.objects.count()
    cantidad_iniciado = Ordenes_Mantenimiento.objects.filter(estado_equipo='iniciado').count()
    cantidad_finalizado = Ordenes_Mantenimiento.objects.filter(estado_equipo='finalizado').count()
    return render(request, 'dashboard/dashboard.html', {
        'cantidad_clientes': cantidad_clientes,
        'cantidad_tipos_equipos': cantidad_tipos_equipos,
        'cantidad_iniciado': cantidad_iniciado,
        'cantidad_finalizado': cantidad_finalizado,
    })


#Clientes
@login_required(login_url='login')
def listarClientes(request):
    palabra = request.POST.get('palabraclave') if request.method == 'POST' else None
    if palabra:
        resultado_busqueda = Clientes.objects.filter(
            Q(nombres__icontains=palabra) |
            Q(apellidos__icontains=palabra) |
            Q(numero_identificacion__icontains=palabra)
        )
    else:
        resultado_busqueda = Clientes.objects.all()
    lista = resultado_busqueda.order_by('-id')
    paginator = Paginator(lista, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clientes/listar.html', {'page_obj': page_obj})




@login_required(login_url = 'login')
def agregarClientes(request):
    if request.method == "POST":
        if (
            request.POST.get("nombres_cliente")
            and request.POST.get("apellidos_cliente")
            and request.POST.get("tipo_identificacion_cliente")
            and request.POST.get("num_identi_cliente")
            and request.POST.get("email_cliente")
            and request.POST.get("celular_cliente")
            and request.POST.get("direcci_cliente")
        ):
            clientes = Clientes()
            clientes.nombres = request.POST.get("nombres_cliente")
            clientes.apellidos = request.POST.get("apellidos_cliente")
            clientes.tipo_identificacion = request.POST.get(
                "tipo_identificacion_cliente"
            )
            clientes.numero_identificacion = request.POST.get("num_identi_cliente")
            clientes.correo_electronico = request.POST.get("email_cliente")
            clientes.celular = request.POST.get("celular_cliente")
            clientes.direccion = request.POST.get("direcci_cliente")
            clientes.save()
            return redirect('listar')
    else:
        return render(request, 'clientes/agregar.html')
    
    
@login_required(login_url = 'login')  
def actualizarCliente(request, id):
    cliente = Clientes.objects.get(id = id)
    datos = {
        'c': cliente,
    }
    return render(request, 'clientes/actualizar.html', datos) 
@login_required(login_url = 'login')
def editarCliente(request):
    if request.method == "POST":
        if (
            request.POST.get("clienteid")
            and request.POST.get("nombres_cliente")
            and request.POST.get("apellidos_cliente")
            and request.POST.get("tipo_identificacion_cliente")
            and request.POST.get("num_identi_cliente")
            and request.POST.get("email_cliente")
            and request.POST.get("celular_cliente")
            and request.POST.get("direcci_cliente")
        ):
            clientes = Clientes()
            clientes.id = request.POST.get("clienteid")
            clientes.nombres = request.POST.get("nombres_cliente")
            clientes.apellidos = request.POST.get("apellidos_cliente")
            clientes.tipo_identificacion = request.POST.get(
                "tipo_identificacion_cliente"
            )
            clientes.numero_identificacion = request.POST.get("num_identi_cliente")
            clientes.correo_electronico = request.POST.get("email_cliente")
            clientes.celular = request.POST.get("celular_cliente")
            clientes.direccion = request.POST.get("direcci_cliente")
            clientes.save()
            return redirect('listar')
        
@login_required(login_url = 'login')
def eliminarCliente (request, id):
    cliente = Clientes.objects.get(id = id)
    cliente.delete()
    return redirect('listar')

@login_required(login_url='login')
def ver_cliente(request, cliente_id):

    cliente = get_object_or_404(Clientes, id=cliente_id)

 
    context = {
        'cliente': cliente,
    }
    return render(request, 'clientes/ver_cliente.html', context)


#TIPO EQUIPOS
@login_required(login_url = 'login')
def listar_tipo_equipos(request):
    if request.method == 'POST':
        palabra = request.POST.get('palabraclave')
        lista = Tipo_equipos.objects.all()
        if palabra is not None:
            resultado_busqueda = lista.filter (
                Q(nombre__icontains = palabra) |
                Q(codigo__icontains = palabra) 
            )
            paginator = Paginator(resultado_busqueda, 7) 
        else:
            paginator = Paginator(lista, 7)  
    else:
        lista = Tipo_equipos.objects.order_by('-id')
        paginator = Paginator(lista, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tipo_equipos/lista_equipos.html', {'page_obj': page_obj})

@login_required(login_url = 'login')
def agregarTipoEquipo(request):
    if request.method == "POST":
        if (
            request.POST.get("nombre_equipo")
            and request.POST.get("codigo_equipo")
        ):
            tipo_equipo = Tipo_equipos()
            tipo_equipo.nombre = request.POST.get("nombre_equipo")
            tipo_equipo.codigo = request.POST.get("codigo_equipo")
            estado_respaldo = request.POST.get("estado_respaldo_equipo")
            tipo_equipo.estado_respaldo = estado_respaldo == "on"
            tipo_equipo.save()
            return redirect('lista_tipo_equipos')
    else:
        return render(request, 'tipo_equipos/agregar_equipo.html')
    
    
    
@login_required(login_url = 'login')   
def actualizarTipoEquipo(request, id):
    tipo_equipos = Tipo_equipos.objects.get(id = id)
    datos = {
        'tipo_equipos': tipo_equipos,
    }
    return render(request, 'tipo_equipos/actualizar_tipo_equipo.html', datos) 

@login_required(login_url = 'login')
def editarTipoOrden(request):
    if request.method == "POST":
        if (
            request.POST.get("tipo_equipos_id")
            and request.POST.get("nombre_equipo")
            and request.POST.get("codigo_equipo")
        ):
            tipo_equipos = Tipo_equipos()
            tipo_equipos.id = request.POST.get("tipo_equipos_id")
            tipo_equipos.nombre = request.POST.get("nombre_equipo")
            tipo_equipos.codigo = request.POST.get("codigo_equipo")
            estado_respaldo = request.POST.get("estado_respaldo_equipo")
            tipo_equipos.estado_respaldo = estado_respaldo == "on"
            tipo_equipos.save()
            return redirect('lista_tipo_equipos')

@login_required(login_url = 'login')     
def eliminarTipoEquipo (request, id):
    tipo_equipos = Tipo_equipos.objects.get(id = id)
    tipo_equipos.delete()
    return redirect('lista_tipo_equipos')

@login_required(login_url='login')
def ver_equipo(request, equipo_id):

    equipo = get_object_or_404(Tipo_equipos, id=equipo_id)


    context = {
        'equipo': equipo,
    }
    return render(request, 'tipo_equipos/ver_equipo.html', context)


#ORDENES
@login_required(login_url = 'login')
def lista_ordenes(request):
    if request.method == 'POST':
        palabra = request.POST.get('palabraclave')
        lista = Ordenes_Mantenimiento.objects.all()
        if palabra is not None:
            resultado_busqueda = lista.filter (
                Q(equipo__nombre__icontains = palabra) |
                Q(cliente__nombres__icontains = palabra) |
                Q(cliente__apellidos__icontains = palabra)
            )
            paginator = Paginator(resultado_busqueda, 7)  # Se envia el resultado de busqueda solo en paginacion 7
        else:
            paginator = Paginator(lista, 7) 
    else:
        lista = Ordenes_Mantenimiento.objects.order_by('-id')
        paginator = Paginator(lista, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ordenes/lista_ordenes.html', {'page_obj': page_obj})


@login_required(login_url='login')
def agregarOrdenMantenimiento(request):
    ultimo_orden = Ordenes_Mantenimiento.objects.all().order_by('id').last()
    if ultimo_orden:
        nuevo_numero_orden = ultimo_orden.id + 1
    else:
        nuevo_numero_orden = 1  

    if request.method == 'POST':

        cliente_id = request.POST.get('cliente')
        equipo_id = request.POST.get('equipo')
        numero_serie = request.POST.get('numero_serie')
        estado_equipo = "Iniciado"
        modelo = request.POST.get('modelo') 
        marca = request.POST.get('marca')
        color = request.POST.get('color')
        contrasena = request.POST.get('contrasena')
        desea_respaldo = request.POST.get('desea_respaldo') == 'on'
        observaciones = request.POST.get('observaciones')
        detalles_dano = request.POST.get('detalles_dano')
        accesorios_seleccionados = request.POST.getlist('accesorios')
        estados_seleccionados = request.POST.getlist('estados')

        cliente = Clientes.objects.get(id=cliente_id)
        equipo = Tipo_equipos.objects.get(id=equipo_id)
        nueva_orden = Ordenes_Mantenimiento(
            cliente=cliente,
            equipo=equipo,
            numero_serie=numero_serie,
            estado_equipo=estado_equipo,
            modelo=modelo,
            marca=marca,
            color=color,
            contrasena=contrasena,
            desea_respaldo=desea_respaldo,
            observaciones=observaciones,
            detalles_dano=detalles_dano,
            trabajo=10,
        )
        nueva_orden.save()

        if accesorios_seleccionados:
            for accesorio_id in accesorios_seleccionados:
                accesorio = Accesorio.objects.get(id=accesorio_id)
                nueva_orden.accesorios.add(accesorio)
        if estados_seleccionados:
            for estado_id in estados_seleccionados:
                estado = Estado.objects.get(id=estado_id)
                nueva_orden.estado.add(estado)

        nueva_orden.save()

        return redirect('lista_ordenes')

    else:
        clientes = Clientes.objects.all()
        equipos = Tipo_equipos.objects.all()
        accesorios = Accesorio.objects.all()
        estados = Estado.objects.all()

        context = {
            'clientes': clientes,
            'equipos': equipos,
            'accesorios': accesorios,
            'estados': estados,
            'nuevo_numero_orden': nuevo_numero_orden,  
        }
        return render(request, 'ordenes/agregar_orden_mantenimiento.html', context)

def obtener_clientes(request, palabraClave=None):
    if palabraClave is None:
        data = {'message': "No se proporcionó ninguna palabra clave"}
    else:
        clientes = list(Clientes.objects.filter(
            Q(numero_identificacion__icontains = palabraClave) |
            Q(nombres__icontains = palabraClave) |
            Q(apellidos__icontains = palabraClave)
        ))
        if clientes:
            clientes_data = [model_to_dict(cliente) for cliente in clientes]
            data = {'message': "Encontrados", 'clientes': clientes_data}
        else:
            data = {'message': "No encontrados"}
    return JsonResponse(data)

@login_required(login_url='login')
def ver_orden_mantenimiento(request, orden_id):
    orden = get_object_or_404(Ordenes_Mantenimiento, id=orden_id)

    context = {
        'orden': orden,
    }
    return render(request, 'ordenes/ver_orden_mantenimiento.html', context)


#Listar mis ordenes
@login_required(login_url = 'login')
def lista_mis_ordenes(request):
    if request.method == 'POST':
        palabra = request.POST.get('palabraclave')
        lista = Ordenes_Mantenimiento.objects.all()
        if palabra is not None:
            resultado_busqueda = lista.filter (
                Q(equipo__nombre__icontains = palabra) |
                Q(cliente__nombres__icontains = palabra) |
                Q(cliente__apellidos__icontains = palabra)
            )
            paginator = Paginator(resultado_busqueda, 7) 
        else:
            paginator = Paginator(lista, 7)  
    else:
        lista = Ordenes_Mantenimiento.objects.order_by('-id')
        paginator = Paginator(lista, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mis_ordenes/lista_mis_ordenes.html', {'page_obj': page_obj})

def orden_detalle(request, orden_id):
    orden_mantenimiento = get_object_or_404(Ordenes_Mantenimiento, id=orden_id)
    diagnósticos = MisOrdenes.objects.filter(orden_mantenimiento=orden_mantenimiento).order_by('-fecha_diagnostico')
    return render(request, 'mis_ordenes/orden_detalle.html', {
        'orden_mantenimiento': orden_mantenimiento,
        'diagnósticos': diagnósticos
    })


@login_required(login_url='login')
def agregarDiagnostico(request, orden_id):
    orden_mantenimiento = get_object_or_404(Ordenes_Mantenimiento, id=orden_id)

    if request.method == 'POST':
        diagnostico = request.POST.get('diagnostico')
        nueva_mis_ordenes = MisOrdenes(
            orden_mantenimiento=orden_mantenimiento,
            diagnostico=diagnostico,
            fecha_diagnostico=timezone.now(),
            usuario=request.user  #
        )
        nueva_mis_ordenes.save()

        orden_mantenimiento.estado_equipo = 'Finalizado'
        orden_mantenimiento.trabajo = 100
        orden_mantenimiento.save()

        return redirect('orden_detalle', orden_id=orden_mantenimiento.id)

    return render(request, 'mis_ordenes/agregar_diagnostico.html', {
        'orden_mantenimiento': orden_mantenimiento,
        'clientes': Clientes.objects.all(),
        'equipos': Tipo_equipos.objects.all(),
        'nuevo_numero_orden': orden_mantenimiento.id
    })



@login_required(login_url='login')
def generar_pdf_orden_mantenimiento(request, orden_id):
    orden = get_object_or_404(Ordenes_Mantenimiento, id=orden_id)
    template = get_template('ordenes/ver_orden_mantenimiento_pdf.html')
    html = template.render({'orden': orden})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=orden_mantenimiento_{orden.id}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)
    return response