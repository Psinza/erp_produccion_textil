from django.urls import path
from . import views

app_name = 'pcpi'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('planificaciones/nueva/', views.planificacion_create, name='planificacion_create'),
    path('planificaciones/<int:pk>/editar/', views.planificacion_update, name='planificacion_update'),
    path('programaciones/nueva/', views.programacion_create, name='programacion_create'),
    path('programaciones/<int:pk>/editar/', views.programacion_update, name='programacion_update'),
    path('resumenes-materiales/nuevo/', views.resumen_create, name='resumen_create'),
    path('resumenes-materiales/<int:pk>/editar/', views.resumen_update, name='resumen_update'),
    path('ordenes-trabajo/<int:pk>/distribuir/', views.distribucion_create, name='distribucion_create'),
]
