from django.contrib import admin
from .models import (
    CategoriaMateriaPrima,
    ProductoTerminado, CategoriaProductoTerminado, OrdenProduccion,
    DepartamentoUDP, DepartamentoCorte, DepartamentoBordado,
    DepartamentoProduccion, DepartamentoDespacho, DepartamentoCalidadISO9001,
    ProcesoDepartamento, IndicadorProceso, MedicionIndicador, Notificacion, NoConformidad,
    CatalogoProceso,
    FichaTecnica, MaterialFichaTecnica,
    LineaProduccion, MaquinaTextil, SolicitudPiezaMecanica,
    OrdenMantenimientoTextil, ChequeoLineaProduccion, PlanMantenimientoTextil,
)

@admin.register(CategoriaMateriaPrima)
class CategoriaMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(CategoriaProductoTerminado)
class CategoriaProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_prenda', 'categoria', 'stock_actual', 'activo')
    list_filter = ('tipo_prenda', 'activo')

class MaterialFichaTecnicaInline(admin.TabularInline):
    model = MaterialFichaTecnica
    extra = 1

@admin.register(FichaTecnica)
class FichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'version', 'metraje_tela_por_unidad', 'consumo_hilo_por_unidad', 'aprobada')
    list_filter = ('aprobada',)
    search_fields = ('producto__nombre', 'producto__sku')
    inlines = [MaterialFichaTecnicaInline]

@admin.register(MaterialFichaTecnica)
class MaterialFichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'materia_prima', 'cantidad_por_unidad', 'desperdicio_porcentaje')

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
admin.site.register(ProcesoDepartamento)
admin.site.register(IndicadorProceso)
admin.site.register(MedicionIndicador)
admin.site.register(Notificacion)
admin.site.register(NoConformidad)
admin.site.register(CatalogoProceso)
admin.site.register(LineaProduccion)
admin.site.register(MaquinaTextil)
admin.site.register(SolicitudPiezaMecanica)
admin.site.register(OrdenMantenimientoTextil)
admin.site.register(ChequeoLineaProduccion)
admin.site.register(PlanMantenimientoTextil)
