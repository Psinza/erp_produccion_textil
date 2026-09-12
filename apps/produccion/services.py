from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.compras.models import DetalleRequerimientoMaterial, RequerimientoMaterial
from .models import DepartamentoUDP, FichaTecnica, MaterialFichaTecnica, OrdenProduccion, ProductoTerminado


@transaction.atomic
def generar_orden_desde_detalle_pedido(detalle, usuario=None):
    """Convierte una línea vendida en orden, ficha/UDP y requerimiento de materiales."""
    if getattr(detalle, 'orden_produccion_id', None):
        return detalle.orden_produccion

    producto = detalle.producto.producto_base
    if not producto:
        raise ValueError('El producto vendido debe estar vinculado a un ProductoTerminado de producción.')

    ficha = FichaTecnica.objects.filter(producto=producto, aprobada=True).first()
    cantidad = Decimal(detalle.cantidad)
    source_number = getattr(getattr(detalle, 'pedido', None), 'numero', None) or getattr(detalle, 'pedido_numero', 'SIN-ORIGEN')
    detail_id = getattr(detalle, 'pk', '0')
    lote = f'PED-{source_number}-{detail_id}'
    pedido_origen = getattr(detalle, 'pedido', None)
    orden = OrdenProduccion.objects.create(
        lote_numero=lote[:50],
        producto=producto,
        cantidad_a_producir=int(cantidad),
        responsable=usuario,
        pedido_origen=pedido_origen,
        observaciones=f'Generada desde {source_number}.',
    )

    udp = DepartamentoUDP.objects.create(
        orden=orden,
        proyecto=f'Pedido {detalle.pedido.numero}',
        tipo_diseno=producto.nombre,
        piezas_por_diseno=int(cantidad),
        ficha_tecnica=f'Ficha aprobada v{ficha.version}' if ficha else 'Nueva prenda: pendiente de completar ficha técnica.',
        requerimiento_materiales='Consumo pendiente de aprobación UDP.' if not ficha else '',
    )

    if ficha:
        requerimiento = RequerimientoMaterial.objects.create(
            numero=f'RM-{orden.lote_numero}'[:30],
            orden_produccion=orden,
            solicitado_por=usuario,
            fecha_requerida=timezone.now().date(),
            observaciones=f'Generado automáticamente desde {detalle.pedido.numero}.',
        )
        for material in ficha.materiales.select_related('materia_prima'):
            DetalleRequerimientoMaterial.objects.create(
                requerimiento=requerimiento,
                materia_prima=material.materia_prima,
                descripcion=material.materia_prima.nombre,
                cantidad=material.cantidad_requerida(cantidad),
                unidad_medida=material.materia_prima.unidad_medida,
                especificacion=material.observaciones,
            )
        udp.requerimiento_materiales = f'{requerimiento.numero}: materiales calculados para {cantidad} unidades.'
        udp.aprobado = True
        udp.save(update_fields=['requerimiento_materiales', 'aprobado'])
        orden.estado = 'en_corte'
        orden.save(update_fields=['estado'])
    return orden


@transaction.atomic
def generar_orden_desde_detalle_cotizacion(detalle, usuario=None):
    class CotizacionContext:
        numero = f'COT-{detalle.cotizacion.numero}'

    class DetalleContext:
        orden_produccion = None
        pedido = None
        producto = detalle.producto
        cantidad = detalle.cantidad
    detalle_context = DetalleContext()
    detalle_context.pedido_numero = CotizacionContext.numero
    return generar_orden_desde_detalle_pedido(detalle_context, usuario)


@transaction.atomic
def generar_requerimiento_desde_ficha(orden, usuario=None):
    ficha = FichaTecnica.objects.filter(
        producto=orden.producto, aprobada=True
    ).prefetch_related('materiales__materia_prima').first()
    if not ficha:
        return None
    requerimiento, _ = RequerimientoMaterial.objects.get_or_create(
        orden_produccion=orden,
        defaults={
            'numero': f'RM-{orden.lote_numero}'[:30],
            'solicitado_por': usuario,
            'fecha_requerida': timezone.now().date(),
            'observaciones': 'Generado desde la ficha técnica aprobada.',
        },
    )
    for material in ficha.materiales.all():
        DetalleRequerimientoMaterial.objects.get_or_create(
            requerimiento=requerimiento,
            materia_prima=material.materia_prima,
            defaults={
                'descripcion': material.materia_prima.nombre,
                'cantidad': material.cantidad_requerida(orden.cantidad_a_producir),
                'unidad_medida': material.materia_prima.unidad_medida,
                'especificacion': material.observaciones,
            },
        )
    return requerimiento
