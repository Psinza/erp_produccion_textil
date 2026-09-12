from django.contrib import admin
from .models import Departamento, Empleado, DocumentoEmpleado

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'departamento', 'cargo', 'activo')
    list_filter = ('departamento', 'activo')
    search_fields = ('cedula', 'nombres', 'apellidos')


@admin.register(DocumentoEmpleado)
class DocumentoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo', 'numero', 'validado', 'fecha_vencimiento', 'creado_en')
    list_filter = ('tipo', 'validado')
