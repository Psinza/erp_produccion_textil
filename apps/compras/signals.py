from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FacturaCompra, DetalleFacturaCompra
from apps.facturacion.models import RetencionIVA, RetencionISLR
from decimal import Decimal
from apps.logistica.models import Almacen, MovimientoInventario

@receiver(post_save, sender=FacturaCompra)
def generar_propuestas_retencion(sender, instance, created, **kwargs):
    """
    Cuando se registra una factura de compra con datos fiscales,
    se generan automáticamente las propuestas de retención de IVA e ISLR.
    """
    if not created or instance.estado == 'anulada':
        return
    # 1. Propuesta de Retención de IVA
    monto_iva = instance.monto_iva_general + instance.monto_iva_reducida + instance.monto_iva_suntuaria
    if monto_iva > 0:
        if not RetencionIVA.objects.filter(nro_factura=instance.numero_factura, proveedor=instance.proveedor).exists():
            RetencionIVA.objects.create(
                nro_comprobante=f"IVA-{instance.id}",
                proveedor=instance.proveedor,
                nro_factura=instance.numero_factura,
                nro_control=instance.numero_control,
                fecha_factura=instance.fecha_emision,
                monto_total_compra=instance.total,
                base_imponible=instance.base_imponible,
                monto_iva=monto_iva,
                porcentaje_retencion=Decimal('75.00'),
            )

    # 2. Propuesta de Retención de ISLR
    if instance.base_imponible > 0:
        if not RetencionISLR.objects.filter(nro_factura=instance.numero_factura, proveedor=instance.proveedor).exists():
            RetencionISLR.objects.create(
                nro_comprobante=f"ISLR-{instance.id}",
                proveedor=instance.proveedor,
                nro_factura=instance.numero_factura,
                fecha_factura=instance.fecha_emision,
                codigo_concepto="000",
                monto_operacion=instance.base_imponible,
                porcentaje_retencion=Decimal('1.00'),
                sustraendo=Decimal('0.00'),
            )


def _almacen_por_articulo(detalle):
    if detalle.factura.almacen_recepcion:
        return detalle.factura.almacen_recepcion
    orden_compra = detalle.factura.orden_compra
    if orden_compra and orden_compra.requerimiento and orden_compra.requerimiento.almacen_destino:
        return orden_compra.requerimiento.almacen_destino
    if detalle.repuesto:
        tipo = 'repuestos'
    elif detalle.materia_prima and detalle.materia_prima.tipo_insumo in ('tela', 'hilo'):
        tipo = 'materias_primas'
    else:
        tipo = 'consumibles'
    return Almacen.objects.filter(tipo=tipo, activo=True).order_by('id').first()


def registrar_entrada_inventario(detalle):
    """Registra una recepción una sola vez por detalle de factura."""
    if detalle.factura.estado == 'anulada':
        return
    almacen = _almacen_por_articulo(detalle)
    if not almacen or (not detalle.materia_prima and not detalle.repuesto):
        return
    referencia = f'Recepción factura {detalle.factura.numero_factura} detalle {detalle.pk}'
    if MovimientoInventario.objects.filter(referencia=referencia).exists():
        return
    movimiento = MovimientoInventario(
        materia_prima=detalle.materia_prima,
        repuesto=detalle.repuesto,
        tipo='E',
        motivo='compra',
        almacen_destino=almacen,
        cantidad=detalle.cantidad,
        referencia=referencia,
        usuario=detalle.factura.registrada_por,
    )
    movimiento.full_clean()
    movimiento.save()


@receiver(post_save, sender=FacturaCompra)
def registrar_detalles_existentes(sender, instance, **kwargs):
    for detalle in instance.detalles.all():
        registrar_entrada_inventario(detalle)


@receiver(post_save, sender=DetalleFacturaCompra)
def registrar_detalle_recibido(sender, instance, **kwargs):
    registrar_entrada_inventario(instance)