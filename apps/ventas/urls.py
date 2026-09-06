from django.urls import path
from apps.ventas.views import (
    dashboard,
    cliente_list,
    cliente_create,
    exportar_clientes_pdf,
    producto_list,
    disponibilidad_productos,
    pedido_list,
    pedido_create,
    cotizacion_list,
    cotizacion_create,
)

app_name = 'ventas'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/reporte-pdf/', exportar_clientes_pdf, name='exportar_clientes_pdf'),
    path('productos/', producto_list, name='producto_list'),
    path('productos/disponibilidad/', disponibilidad_productos, name='disponibilidad'),
    path('pedidos/', pedido_list, name='pedido_list'),
    path('pedidos/nuevo/', pedido_create, name='pedido_create'),
    path('cotizaciones/', cotizacion_list, name='cotizacion_list'),
    path('cotizaciones/nueva/', cotizacion_create, name='cotizacion_create'),
]