from django.contrib import admin
from .models import CategoriaComercial, InformacionComercial, ListaPrecio, ItemPrecio, OrdenProduccionComercial, EncuestaSatisfaccionCliente

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
