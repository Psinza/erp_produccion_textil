from django.urls import path
from . import views

app_name = 'calidad'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('auditorias/nueva/', views.auditoria_create, name='auditoria_create'),
    path('ordenes/<int:pk>/auditoria/nueva/', views.auditoria_create, name='auditoria_create_orden'),
    path('auditorias/<int:pk>/', views.auditoria_detail, name='auditoria_detail'),
]
