from django.contrib import admin
from .models import (
    ProductoCompra, OrdenCompra, FacturaCompra, DetalleFacturaCompra,
    RequerimientoMaterial, DetalleRequerimientoMaterial,
    DetalleOrdenCompra, RecepcionCompra, DetalleRecepcionCompra,
)

@admin.register(ProductoCompra)
class ProductoCompraAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "tipo", "unidad_medida", "precio_referencia"]
    search_fields = ["codigo", "nombre"]

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ["numero", "proveedor", "fecha_emision", "estado", "total"]
    list_filter = ["estado"]
    search_fields = ["numero", "proveedor__razon_social"]


class DetalleRequerimientoInline(admin.TabularInline):
    model = DetalleRequerimientoMaterial
    extra = 1


@admin.register(RequerimientoMaterial)
class RequerimientoMaterialAdmin(admin.ModelAdmin):
    list_display = ["numero", "orden_produccion", "estado", "fecha_requerida"]
    list_filter = ["estado"]
    search_fields = ["numero", "orden_produccion__lote_numero"]
    inlines = [DetalleRequerimientoInline]


class DetalleOrdenCompraInline(admin.TabularInline):
    model = DetalleOrdenCompra
    extra = 1


class DetalleRecepcionInline(admin.TabularInline):
    model = DetalleRecepcionCompra
    extra = 1


@admin.register(RecepcionCompra)
class RecepcionCompraAdmin(admin.ModelAdmin):
    list_display = ['numero_acta', 'orden', 'almacen', 'fecha', 'estado', 'recibido_por']
    list_filter = ['estado', 'almacen']
    search_fields = ['numero_acta', 'orden__numero']
    inlines = [DetalleRecepcionInline]

class DetalleFacturaCompraInline(admin.TabularInline):
    model = DetalleFacturaCompra
    extra = 1

@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    list_display = ["numero_factura", "proveedor", "orden_compra", "almacen_recepcion", "fecha_emision", "estado", "total"]
    list_filter = ["estado"]
    search_fields = ["numero_factura", "numero_control", "proveedor__razon_social"]
    inlines = [DetalleFacturaCompraInline]
