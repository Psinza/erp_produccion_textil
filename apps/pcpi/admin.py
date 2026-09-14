from django.contrib import admin
from .models import (
    PlanificacionEntrega, ProgramacionSemanal,
    ResumenRequerimientosMateriales, DistribucionOrdenTrabajo,
)


@admin.register(PlanificacionEntrega)
class PlanificacionEntregaAdmin(admin.ModelAdmin):
    list_display = ('orden', 'fecha_entrega_comprometida', 'dias_habiles_requeridos', 'estado', 'responsable')
    list_filter = ('estado',)
    search_fields = ('orden__lote_numero',)


@admin.register(ProgramacionSemanal)
class ProgramacionSemanalAdmin(admin.ModelAdmin):
    list_display = ('semana_inicio', 'semana_fin', 'planificacion', 'cuotas_produccion', 'estado')
    list_filter = ('estado',)


@admin.register(ResumenRequerimientosMateriales)
class ResumenRequerimientosMaterialesAdmin(admin.ModelAdmin):
    list_display = ('numero', 'orden', 'estado', 'elaborado_por', 'validado_por')
    list_filter = ('estado',)
    search_fields = ('numero', 'orden__lote_numero')


@admin.register(DistribucionOrdenTrabajo)
class DistribucionOrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('orden_trabajo', 'unidad', 'recibido', 'fecha_entrega')
    list_filter = ('recibido',)
