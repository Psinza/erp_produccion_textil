from django.contrib import admin
from .models import AuditoriaCalidad


@admin.register(AuditoriaCalidad)
class AuditoriaCalidadAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_inspeccion', 'procedimiento', 'orden', 'estado',
        'piezas_aprobadas', 'piezas_rechazadas', 'inspector',
    )
    list_filter = ('procedimiento', 'estado', 'fecha_inspeccion')
    search_fields = ('orden__lote_numero', 'numero_orden_trabajo', 'cliente', 'descripcion_prenda')
