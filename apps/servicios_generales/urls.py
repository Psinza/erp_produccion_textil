from django.urls import path

from . import views

app_name = 'servicios_generales'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<slug:resource>/', views.resource_list, name='resource_list'),
    path('<slug:resource>/nuevo/', views.resource_create, name='resource_create'),
    path('<slug:resource>/<int:pk>/editar/', views.resource_update, name='resource_update'),
]
