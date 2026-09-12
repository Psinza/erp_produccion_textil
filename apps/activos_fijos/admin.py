from django.contrib import admin
from .models import ActivoFijo, CategoriaActivo


@admin.register(CategoriaActivo)
class CategoriaActivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'prefijo_codigo', 'vida_util_defecto']
    search_fields = ['nombre', 'prefijo_codigo']

@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'fecha_adquisicion', 'valor_compra', 'estado']
    search_fields = ['codigo', 'nombre']
    list_filter = ['categoria', 'estado', 'fecha_adquisicion']