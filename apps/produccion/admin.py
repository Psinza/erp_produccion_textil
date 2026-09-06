from django.contrib import admin
from .models import (
    ProductoTerminado, CategoriaProductoTerminado, OrdenProduccion,
    DepartamentoUDP, DepartamentoCorte, DepartamentoBordado,
    DepartamentoProduccion, DepartamentoDespacho, DepartamentoCalidadISO9001
)

@admin.register(CategoriaProductoTerminado)
class CategoriaProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_prenda', 'categoria', 'stock_actual', 'activo')
    list_filter = ('tipo_prenda', 'activo')

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('lote_numero', 'producto', 'cantidad_a_producir', 'estado', 'prioridad', 'piezas_producidas_ok', 'piezas_rechazadas')
    list_filter = ('estado', 'prioridad')
    search_fields = ('lote_numero', 'producto__nombre')

admin.site.register(DepartamentoUDP)
admin.site.register(DepartamentoCorte)
admin.site.register(DepartamentoBordado)
admin.site.register(DepartamentoProduccion)
admin.site.register(DepartamentoDespacho)
admin.site.register(DepartamentoCalidadISO9001)
