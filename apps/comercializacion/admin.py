from django.contrib import admin
from .models import (
    CategoriaComercial, InformacionComercial, ListaPrecio, ItemPrecio,
    OrdenProduccionComercial, EncuestaSatisfaccionCliente, SolicitudCotizacion,
    CotizacionComercial, ReclamoComercial, SolicitudDonacion,
)

@admin.register(CategoriaComercial)
class CategoriaComercialAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(InformacionComercial)
class InformacionComercialAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'producto', 'categoria', 'en_oferta', 'destacado')
    list_filter = ('categoria', 'en_oferta', 'destacado')
    search_fields = ('nombre_comercial', 'producto__nombre')

@admin.register(ListaPrecio)
class ListaPrecioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'moneda', 'factor_ajuste', 'activa')
    list_filter = ('moneda', 'activa')

@admin.register(ItemPrecio)
class ItemPrecioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'lista', 'precio', 'descuento_maximo')
    list_filter = ('lista',)
    search_fields = ('producto__nombre_comercial',)


@admin.register(OrdenProduccionComercial)
class OrdenProduccionComercialAdmin(admin.ModelAdmin):
    list_display = ('numero', 'producto', 'cliente', 'fecha', 'fecha_entrega', 'cantidad_total', 'estado', 'orden_produccion')
    list_filter = ('estado', 'fecha')
    search_fields = ('numero', 'cliente', 'producto__nombre')


@admin.register(EncuestaSatisfaccionCliente)
class EncuestaSatisfaccionClienteAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'organizacion', 'representante', 'calidad_servicio', 'producto_servicio')
    list_filter = ('fecha', 'calidad_servicio', 'producto_servicio')
    search_fields = ('organizacion', 'representante', 'correo')


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'tipo', 'fecha_recepcion', 'estado')
    list_filter = ('tipo', 'estado')
    search_fields = ('numero', 'cliente', 'correo')


@admin.register(CotizacionComercial)
class CotizacionComercialAdmin(admin.ModelAdmin):
    list_display = ('numero', 'solicitud', 'fecha', 'vigencia_hasta', 'estado', 'aprobada_por_cliente')
    list_filter = ('estado', 'moneda', 'aprobada_por_cliente')
    search_fields = ('numero', 'solicitud__cliente')


@admin.register(ReclamoComercial)
class ReclamoComercialAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha_recepcion', 'fecha_limite_respuesta', 'estado')
    list_filter = ('estado', 'canal')
    search_fields = ('numero', 'cliente', 'asunto')


@admin.register(SolicitudDonacion)
class SolicitudDonacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'beneficiario', 'institucion_solicitante', 'fecha_solicitud', 'estado')
    list_filter = ('estado', 'aprobacion_presidencia')
    search_fields = ('numero', 'beneficiario', 'institucion_solicitante')
