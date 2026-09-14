from django.urls import path
from . import views

app_name = 'logistica'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
    path('solicitudes/', views.solicitud_list, name='solicitud_list'),
    path('solicitudes/nueva/', views.solicitud_create, name='solicitud_create'),
    path('solicitudes/<int:pk>/editar/', views.solicitud_update, name='solicitud_update'),
    path('recepciones/nueva/', views.recepcion_create, name='recepcion_create'),
    path('recepciones/<int:pk>/editar/', views.recepcion_update, name='recepcion_update'),
    path('despachos/nuevo/', views.despacho_create, name='despacho_create'),
    path('despachos/<int:pk>/editar/', views.despacho_update, name='despacho_update'),
    path('operaciones/', views.operaciones_list, name='operaciones_list'),
    path('almacen-maquinas/', views.repuesto_list, name='repuesto_list'),
    path('almacen-maquinas/piezas/nueva/', views.repuesto_create, name='repuesto_create'),
    path('almacen-maquinas/piezas/<int:pk>/editar/', views.repuesto_update, name='repuesto_update'),
    path('almacenes/', views.almacen_list, name='almacen_list'),
    path('almacenes/nuevo/', views.almacen_create, name='almacen_create'),
    path('almacenes/<int:pk>/editar/', views.almacen_update, name='almacen_update'),
    path('reporte/stock/', views.reporte_stock, name='reporte_stock'),
    path('reporte/kardex/', views.reporte_kardex, name='reporte_kardex'),
    path('transferencias/nueva/', views.transferencia_create, name='transferencia_create'),
]