from django.urls import path
from apps.ventas.views import (
    dashboard,
    cliente_list,
    cliente_create,
    categoria_cliente_list,
    categoria_cliente_create,
    categoria_cliente_edit,
    exportar_clientes_pdf,
    producto_list,
    producto_create,
    producto_update,
    disponibilidad_productos,
    pedido_list,
    pedido_create,
    generar_produccion_pedido,
    generar_produccion_cotizacion,
    cotizacion_list,
    cotizacion_create,
)

app_name = 'ventas'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('categorias-clientes/', categoria_cliente_list, name='categoria_cliente_list'),
    path('categorias-clientes/nueva/', categoria_cliente_create, name='categoria_cliente_create'),
    path('categorias-clientes/<int:pk>/editar/', categoria_cliente_edit, name='categoria_cliente_edit'),
    path('clientes/reporte-pdf/', exportar_clientes_pdf, name='exportar_clientes_pdf'),
    path('productos/', producto_list, name='producto_list'),
    path('productos/nuevo/', producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', producto_update, name='producto_update'),
    path('productos/disponibilidad/', disponibilidad_productos, name='disponibilidad'),
    path('pedidos/', pedido_list, name='pedido_list'),
    path('pedidos/nuevo/', pedido_create, name='pedido_create'),
    path('pedidos/<int:pk>/generar-produccion/', generar_produccion_pedido, name='generar_produccion'),
    path('cotizaciones/', cotizacion_list, name='cotizacion_list'),
    path('cotizaciones/nueva/', cotizacion_create, name='cotizacion_create'),
    path('cotizaciones/<int:pk>/generar-produccion/', generar_produccion_cotizacion, name='generar_produccion_cotizacion'),
]