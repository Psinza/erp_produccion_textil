from django.contrib import admin
from .models import (
    Almacen, MovimientoInventario, RepuestoMaquina,
    SolicitudAbastecimiento, RecepcionLogistica, DespachoLogistico,
)

admin.site.register(RepuestoMaquina)
admin.site.register(SolicitudAbastecimiento)
admin.site.register(RecepcionLogistica)
admin.site.register(DespachoLogistico)


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'ubicacion', 'es_principal')
    list_editable = ('es_principal',)
    search_fields = ('nombre', 'ubicacion')


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'almacen_origen', 'almacen_destino', 'producto_pt', 'materia_prima', 'repuesto', 'cantidad', 'fecha')
    list_filter = ('tipo', 'almacen_origen', 'almacen_destino')
    date_hierarchy = 'fecha'
    search_fields = ('motivo',)
