from django.urls import path
from . import views

app_name = 'produccion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ordenes/', views.orden_list, name='orden_list'),
    path('ordenes/nueva/', views.orden_create, name='orden_create'),
    path('ordenes/<int:pk>/', views.orden_detail, name='orden_detail'),
    
    # Rutas por Departamentos
    path('ordenes/<int:pk>/udp/', views.gestionar_udp, name='gestionar_udp'),
    path('ordenes/<int:pk>/corte/', views.gestionar_corte, name='gestionar_corte'),
    path('ordenes/<int:pk>/bordado/', views.gestionar_bordado, name='gestionar_bordado'),
    path('ordenes/<int:pk>/produccion/', views.gestionar_produccion, name='gestionar_produccion'),
    path('ordenes/<int:pk>/despacho/', views.gestionar_despacho, name='gestionar_despacho'),
    path('ordenes/<int:pk>/calidad/', views.gestionar_calidad, name='gestionar_calidad'),
    
    path('productos-terminados/', views.producto_terminado_list, name='producto_terminado_list'),
]