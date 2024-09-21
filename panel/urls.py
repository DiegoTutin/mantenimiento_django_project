from django.contrib import admin
from django.urls import path
from django import views
from . import views

#Importacion para cambio de contraseña

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="index"),
    path('registro', views.registroUsuarios, name= "registro"),
    path('login', views.inicioSesion, name="login"),
    path('logout', views.cerrarSesion, name="logout"),
    
    
    path('dashboard', views.dashboard, name='dashboard'),
    
    #PATHS PARA CLIENTE
    path('listar', views.listarClientes, name= "listar"),
    path('agregar', views.agregarClientes, name="agregar"),
    path('actualizarcliente/<int:id>', views.actualizarCliente, name="actualizarcliente"),
    path('editarcliente/', views.editarCliente, name="editarcliente"),
    path('eliminarcliente/<int:id>', views.eliminarCliente, name="eliminarcliente"),
    path('ver_cliente/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    
    #PATHS TIPO EQUIPOS
    path('lista_tipo_equipos', views.listar_tipo_equipos, name= "lista_tipo_equipos"),
    path('agregar_tipo_equipo', views.agregarTipoEquipo, name="agregar_tipo_equipo"),
    path('actualizarTipoEquipo/<int:id>', views.actualizarTipoEquipo, name="actualizarTipoEquipo"),
    path('editarTipoOrden/', views.editarTipoOrden, name="editarTipoOrden"),
    path('eliminarTipoEquipo/<int:id>', views.eliminarTipoEquipo, name="eliminarTipoEquipo"),
    path('ver_equipo/<int:equipo_id>/', views.ver_equipo, name='ver_equipo'),
    
    
    #PATHS ORDENES
    path('lista_ordenes', views.lista_ordenes, name= "lista_ordenes"),
    path('agregar_orden_mantenimiento', views.agregarOrdenMantenimiento, name="agregar_orden_mantenimiento"),
    path('ver_orden/<int:orden_id>/', views.ver_orden_mantenimiento, name='ver_orden_mantenimiento'),
    path('ver_orden/<int:orden_id>/pdf/', views.generar_pdf_orden_mantenimiento, name='generar_pdf_orden_mantenimiento'),
    
    #PATHS MIS ORDENES
    path('lista_mis_ordenes', views.lista_mis_ordenes, name= "lista_mis_ordenes"),
    path('ver_orden/<int:orden_id>/agregar-diagnostico/', views.agregarDiagnostico, name='agregar_diagnostico'),
    path('orden_detalle/<int:orden_id>/', views.orden_detalle, name='orden_detalle'),
    
    #BUSCAR CLIENTES DENTRO DE ORDENES:
    path('obtener_clientes/<str:palabraClave>/', views.obtener_clientes, name='obtener_clientes'),

    #PATHS PARA CAMBIO DE CONTRASEÑA
    path('recuperar_contrasena/', auth_views.PasswordResetView.as_view(template_name="usuarios/recuperar_contra_form.html"), name="recuperar_contrasena"),
    path('cambio_contrasena_enviado/', auth_views.PasswordResetDoneView.as_view(template_name="usuarios/cambio_contra_realizado.html"), name="password_reset_done"),
    path('nueva_contrasena/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="usuarios/nueva_contra_form.html"), name="password_reset_confirm"),
    path('contrasena_cambiada/', auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/cambio_contra_completo.html"), name="password_reset_complete"), 



]
                            
                            