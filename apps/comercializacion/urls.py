from django.urls import path
from . import views

app_name = 'comercializacion'

urlpatterns = [
    path('', views.dashboard_comercializacion, name='dashboard'),
    path('ordenes-produccion/', views.orden_produccion_list, name='orden_produccion_list'),
    path('ordenes-produccion/nueva/', views.orden_produccion_create, name='orden_produccion_create'),
    path('ordenes-produccion/<int:pk>/', views.orden_produccion_detail, name='orden_produccion_detail'),
    path('ordenes-produccion/<int:pk>/editar/', views.orden_produccion_update, name='orden_produccion_update'),
    path('ordenes-produccion/<int:pk>/enviar/', views.enviar_a_produccion, name='enviar_a_produccion'),
    path('encuestas-satisfaccion/', views.encuesta_list, name='encuesta_list'),
    path('encuestas-satisfaccion/nueva/', views.encuesta_create, name='encuesta_create'),
    path('encuestas-satisfaccion/<int:pk>/editar/', views.encuesta_create, name='encuesta_update'),
    
    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    
    # Información Comercial (Catálogo)
    path('productos/', views.producto_comercial_list, name='catalogo_list'),
    path('productos/crear/', views.producto_comercial_create, name='catalogo_create'),
    path('productos/<int:pk>/editar/', views.producto_comercial_update, name='catalogo_edit'),
    path('productos/<int:pk>/eliminar/', views.producto_comercial_delete, name='catalogo_delete'),
    
    # Listas de Precio
    path('listas/', views.lista_precio_list, name='lista_precio_list'),
    path('listas/crear/', views.lista_precio_create, name='lista_precio_create'),
    path('listas/<int:pk>/editar/', views.lista_precio_update, name='lista_precio_update'),
    path('listas/<int:pk>/eliminar/', views.lista_precio_delete, name='lista_precio_delete'),
    path('listas/<int:pk>/detalle/', views.item_precio_list, name='lista_precio_detail'),
    path('listas/<int:pk>/imprimir/', views.lista_imprimir, name='lista_imprimir'),
    
    # Items de Precio
    path('listas/<int:lista_id>/items/', views.item_precio_list, name='item_precio_list'),
    path('listas/<int:lista_id>/items/crear/', views.item_precio_create, name='item_precio_create'),
    path('items/<int:pk>/editar/', views.item_precio_update, name='item_precio_update'),
    path('items/<int:pk>/eliminar/', views.item_precio_delete, name='item_precio_delete'),

    # Promociones
    path('promociones/crear/', views.promocion_create, name='promocion_create'),
    path('manual-procedimientos/', views.manual_procedimientos, name='manual_procedimientos'),
    path('solicitudes-cotizacion/', views.solicitudes_cotizacion, name='solicitudes_cotizacion'),
    path('solicitudes-cotizacion/nueva/', views.solicitud_cotizacion_edit, name='solicitud_cotizacion_create'),
    path('solicitudes-cotizacion/<int:pk>/editar/', views.solicitud_cotizacion_edit, name='solicitud_cotizacion_update'),
    path('cotizaciones/', views.cotizaciones, name='cotizaciones'),
    path('cotizaciones/nueva/', views.cotizacion_edit, name='cotizacion_create'),
    path('cotizaciones/<int:pk>/editar/', views.cotizacion_edit, name='cotizacion_update'),
    path('reclamos/', views.reclamos, name='reclamos'),
    path('reclamos/nuevo/', views.reclamo_edit, name='reclamo_create'),
    path('reclamos/<int:pk>/editar/', views.reclamo_edit, name='reclamo_update'),
    path('donaciones/', views.donaciones, name='donaciones'),
    path('donaciones/nueva/', views.donacion_edit, name='donacion_create'),
    path('donaciones/<int:pk>/editar/', views.donacion_edit, name='donacion_update'),
    path('estadisticas-venta/', views.estadisticas_venta, name='estadisticas_venta'),
]