from django.urls import path
from . import views

app_name = 'logistica'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
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