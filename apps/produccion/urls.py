from django.urls import path
from . import views

app_name = 'produccion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manual/', views.manual_produccion, name='manual_produccion'),
    path('registros-turno/', views.registro_turno_list, name='registro_turno_list'),
    path('registros-turno/nuevo/', views.registro_turno_create, name='registro_turno_create'),
    path('registros-turno/<int:pk>/editar/', views.registro_turno_update, name='registro_turno_update'),
    path('ordenes/', views.orden_list, name='orden_list'),
    path('ordenes/nueva/', views.orden_create, name='orden_create'),
    path('ordenes/<int:pk>/', views.orden_detail, name='orden_detail'),
    
    # Rutas por Departamentos
    path('ordenes/<int:pk>/udp/', views.gestionar_udp, name='gestionar_udp'),
    path('ordenes/<int:pk>/muestra/', views.gestionar_muestra, name='gestionar_muestra'),
    path('ordenes/<int:pk>/digitalizacion/', views.gestionar_digitalizacion, name='gestionar_digitalizacion'),
    path('ordenes/<int:pk>/programacion/', views.gestionar_programacion, name='gestionar_programacion'),
    path('ordenes/<int:pk>/orden-trabajo/', views.gestionar_orden_trabajo, name='gestionar_orden_trabajo'),
    path('ordenes/<int:pk>/corte/', views.gestionar_corte, name='gestionar_corte'),
    path('ordenes/<int:pk>/bordado/', views.gestionar_bordado, name='gestionar_bordado'),
    path('ordenes/<int:pk>/produccion/', views.gestionar_produccion, name='gestionar_produccion'),
    path('ordenes/<int:pk>/despacho/', views.gestionar_despacho, name='gestionar_despacho'),
    path('ordenes/<int:pk>/despacho/nota-entrega/', views.nota_entrega, name='nota_entrega'),
    path('ordenes/<int:pk>/calidad/', views.gestionar_calidad, name='gestionar_calidad'),
    
    path('productos-terminados/', views.producto_terminado_list, name='producto_terminado_list'),
    path('productos-terminados/nuevo/', views.producto_terminado_create, name='producto_terminado_create'),
    path('productos-terminados/<int:pk>/editar/', views.producto_terminado_edit, name='producto_terminado_edit'),
    path('procesos/', views.proceso_list, name='proceso_list'),
    path('ordenes/<int:pk>/procesos/nuevo/', views.proceso_create, name='proceso_create'),
    path('indicadores/', views.indicador_dashboard, name='indicador_dashboard'),
    path('indicadores/medir/', views.indicador_medicion_create, name='indicador_medicion_create'),
    path('indicadores/mediciones/<int:pk>/editar/', views.indicador_medicion_update, name='indicador_medicion_update'),
    path('notificaciones/', views.notificacion_list, name='notificacion_list'),
    path('no-conformidades/', views.no_conformidad_list, name='no_conformidad_list'),
    path('ordenes/<int:pk>/no-conformidad/', views.no_conformidad_create, name='no_conformidad_create'),
    path('no-conformidades/nueva/', views.no_conformidad_create, name='no_conformidad_create_general'),
    path('mecanica/', views.mecanica_dashboard, name='mecanica_dashboard'),
    path('mecanica/maquinas/nueva/', views.mecanica_maquina_create, name='mecanica_maquina_create'),
    path('mecanica/lineas/nueva/', views.mecanica_linea_create, name='mecanica_linea_create'),
    path('mecanica/piezas/nueva/', views.mecanica_solicitud_create, name='mecanica_solicitud_create'),
    path('mecanica/mantenimientos/nuevo/', views.mecanica_mantenimiento_create, name='mecanica_mantenimiento_create'),
    path('mecanica/chequeos/nuevo/', views.mecanica_chequeo_create, name='mecanica_chequeo_create'),
    path('mecanica/planes/nuevo/', views.mecanica_plan_create, name='mecanica_plan_create'),
    path('mecanica/minutas/nueva/', views.mecanica_minuta_create, name='mecanica_minuta_create'),
    path('mecanica/traslados/nuevo/', views.mecanica_traslado_create, name='mecanica_traslado_create'),
    path('mecanica/diagnosticos/nuevo/', views.mecanica_diagnostico_create, name='mecanica_diagnostico_create'),
]