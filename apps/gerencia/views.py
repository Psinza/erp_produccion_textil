from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Sum, Avg, F, ExpressionWrapper, DurationField
from django.shortcuts import render
from django.utils import timezone


@login_required
def dashboard(request):
    from apps.activos_fijos.models import ActivoFijo
    from apps.compras.models import OrdenCompra, RecepcionCompra
    from apps.logistica.models import MovimientoInventario
    from apps.produccion.models import OrdenProduccion, OrdenMantenimientoTextil
    from apps.rrhh.models import Empleado, Nomina
    from apps.transportes.models import Despacho
    from apps.ventas.models import Pedido

    hoy = timezone.localdate()
    inicio = hoy.replace(day=1)
    ordenes = OrdenProduccion.objects.all()
    completadas = ordenes.filter(estado='completada', fecha_inicio__isnull=False, fecha_fin__isnull=False)
    tiempo_produccion = completadas.annotate(
        duracion=ExpressionWrapper(F('fecha_fin') - F('fecha_inicio'), output_field=DurationField())
    ).aggregate(promedio=Avg('duracion'))['promedio']
    compras_recibidas = OrdenCompra.objects.filter(estado='recibida')

    ventas_mes = Pedido.objects.filter(fecha_pedido__gte=inicio).aggregate(total=Sum('total'))['total'] or Decimal('0')
    compras_mes = OrdenCompra.objects.filter(fecha_emision__gte=inicio).aggregate(total=Sum('total'))['total'] or Decimal('0')
    costo_produccion = ordenes.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('cantidad_a_producir') * F('producto__costo_estimado'),
                output_field=models.DecimalField(max_digits=18, decimal_places=2),
            )
        )
    )['total'] or Decimal('0')
    nomina_mes = Nomina.objects.filter(anio=hoy.year, mes=hoy.month).aggregate(total=Sum('total_nomina'))['total'] or Decimal('0')
    movimientos = MovimientoInventario.objects.filter(fecha__date__gte=inicio)
    compras_dias = []
    for compra in compras_recibidas.select_related('requerimiento').prefetch_related('recepciones'):
        recepcion = compra.recepciones.order_by('fecha').first()
        if recepcion:
            compras_dias.append((recepcion.fecha - compra.fecha_emision).days)

    context = {
        'inicio': inicio,
        'ventas_mes': ventas_mes,
        'compras_mes': compras_mes,
        'resultado_mes': ventas_mes - compras_mes - costo_produccion - nomina_mes,
        'costo_produccion': costo_produccion,
        'nomina_mes': nomina_mes,
        'ordenes_total': ordenes.count(),
        'ordenes_activas': ordenes.exclude(estado__in=['completada', 'anulada']).count(),
        'ordenes_completadas': ordenes.filter(estado='completada').count(),
        'unidades_producidas': ordenes.aggregate(total=Sum('piezas_producidas_ok'))['total'] or 0,
        'unidades_rechazadas': ordenes.aggregate(total=Sum('piezas_rechazadas'))['total'] or 0,
        'tiempo_produccion': tiempo_produccion,
        'compras_pendientes': OrdenCompra.objects.exclude(estado__in=['recibida']).count(),
        'compras_recibidas': compras_recibidas.count(),
        'despachos_total': Despacho.objects.count(),
        'despachos_pendientes': Despacho.objects.exclude(estado__in=['entregado', 'completado']).count(),
        'movimientos_almacen': movimientos.count(),
        'entradas_almacen': movimientos.filter(tipo='E').aggregate(total=Sum('cantidad'))['total'] or 0,
        'salidas_almacen': movimientos.filter(tipo='S').aggregate(total=Sum('cantidad'))['total'] or 0,
        'empleados_activos': Empleado.objects.filter(activo=True).count(),
        'activos_total': ActivoFijo.objects.count(),
        'activos_valor': ActivoFijo.objects.aggregate(total=Sum('valor_compra'))['total'] or Decimal('0'),
        'reparaciones': OrdenMantenimientoTextil.objects.count(),
        'reparaciones_pendientes': OrdenMantenimientoTextil.objects.exclude(estado__in=['completada', 'cancelada']).count(),
        'pedidos_pendientes': Pedido.objects.exclude(estado__in=['entregado', 'cancelado']).count(),
        'compras_dias': compras_dias,
    }
    return render(request, 'gerencia/dashboard.html', context)
