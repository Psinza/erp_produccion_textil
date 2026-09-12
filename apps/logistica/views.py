from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Panel principal del módulo de Logística."""
    try:
        from apps.logistica.models import Almacen, MovimientoInventario, ExistenciaAlmacen, RepuestoMaquina
        from apps.produccion.models import MateriaPrima, ProductoTerminado
        from django.db.models import F, Sum

        almacenes = Almacen.objects.all()
        movimientos_recientes = MovimientoInventario.objects.order_by('-fecha')[:10]

        # Valor total de MP basado en existencias
        valor_total_mp = ExistenciaAlmacen.objects.aggregate(
            total=Sum('stock')
        )['total'] or 0

        # Alertas de stock bajo
        materias_primas_alerta = MateriaPrima.objects.filter(
            stock_actual__lte=10
        )
        alerta_mp = materias_primas_alerta.count()
        repuestos_alerta = RepuestoMaquina.objects.filter(
            activo=True, stock_actual__lte=F('stock_minimo')
        )
        total_pt = ProductoTerminado.objects.count()
    except Exception:
        almacenes = []
        movimientos_recientes = []
        valor_total_mp = 0
        materias_primas_alerta = []
        repuestos_alerta = []
        alerta_mp = 0
        total_pt = 0

    return render(request, 'logistica/dashboard.html', {
        'titulo': 'Inventario y Almacén',
        'almacenes': almacenes,
        'movimientos_recientes': movimientos_recientes,
        'valor_total_mp': valor_total_mp,
        'materias_primas_alerta': materias_primas_alerta,
        'repuestos_alerta': repuestos_alerta,
        'alerta_mp': alerta_mp,
        'total_pt': total_pt,
    })


@login_required
def movimiento_list(request):
    try:
        from apps.logistica.models import MovimientoInventario
        movimientos = MovimientoInventario.objects.order_by('-fecha')
    except Exception:
        movimientos = []
    return render(request, 'logistica/movimiento_list.html', {
        'titulo': 'Movimientos de Inventario',
        'movimientos': movimientos,
    })


@login_required
def movimiento_create(request):
    from .forms import MovimientoInventarioForm
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            mov.usuario = request.user
            mov.save()
            return redirect('logistica:movimiento_list')
    else:
        initial = {}
        if request.GET.get('mp'):
            initial = {'item_tipo': 'mp', 'materia_prima': request.GET['mp']}
        elif request.GET.get('pt'):
            initial = {'item_tipo': 'pt', 'producto_pt': request.GET['pt']}
        elif request.GET.get('repuesto'):
            initial = {'item_tipo': 'repuesto', 'repuesto': request.GET['repuesto']}
        if request.GET.get('almacen_destino'):
            initial['almacen_destino'] = request.GET['almacen_destino']
        if request.GET.get('almacen_origen'):
            initial['almacen_origen'] = request.GET['almacen_origen']
        form = MovimientoInventarioForm(initial=initial)
    return render(request, 'logistica/movimiento_form.html', {
        'titulo': 'Nuevo Movimiento de Inventario',
        'form': form
    })


@login_required
def repuesto_list(request):
    from .models import Almacen, ExistenciaAlmacen, MovimientoInventario, RepuestoMaquina

    almacen = Almacen.objects.filter(
        tipo='repuestos', activo=True
    ).order_by('-es_principal', 'id').first()
    repuestos = RepuestoMaquina.objects.filter(activo=True).order_by('nombre')
    existencias = {
        item.repuesto_id: item.stock
        for item in ExistenciaAlmacen.objects.filter(
            almacen=almacen, repuesto__in=repuestos
        )
    } if almacen else {}
    for pieza in repuestos:
        pieza.stock_almacen = existencias.get(pieza.pk, 0)
    movimientos = MovimientoInventario.objects.filter(
        repuesto__isnull=False
    ).select_related('repuesto', 'almacen_origen', 'almacen_destino').order_by('-fecha')[:30]
    return render(request, 'logistica/repuesto_list.html', {
        'titulo': 'Almacén de Repuestos de Máquinas',
        'almacen': almacen,
        'repuestos': repuestos,
        'existencias': existencias,
        'movimientos': movimientos,
    })


@login_required
def repuesto_create(request):
    from .forms import RepuestoMaquinaForm
    form = RepuestoMaquinaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('logistica:repuesto_list')
    return render(request, 'logistica/repuesto_form.html', {
        'titulo': 'Nueva Pieza de Máquina',
        'form': form,
    })


@login_required
def repuesto_update(request, pk):
    from .forms import RepuestoMaquinaForm
    from .models import RepuestoMaquina
    repuesto = get_object_or_404(RepuestoMaquina, pk=pk)
    form = RepuestoMaquinaForm(request.POST or None, instance=repuesto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('logistica:repuesto_list')
    return render(request, 'logistica/repuesto_form.html', {
        'titulo': 'Editar Pieza de Máquina',
        'form': form,
        'repuesto': repuesto,
    })


@login_required
def almacen_list(request):
    try:
        from apps.logistica.models import Almacen
        almacenes = Almacen.objects.all()
    except Exception:
        almacenes = []
    return render(request, 'logistica/almacen_list.html', {
        'titulo': 'Gestión de Almacenes',
        'almacenes': almacenes,
    })


@login_required
def almacen_create(request):
    from .forms import AlmacenForm
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logistica:almacen_list')
    else:
        form = AlmacenForm()
    return render(request, 'logistica/almacen_form.html', {
        'titulo': 'Nuevo Almacén',
        'form': form
    })


@login_required
def almacen_update(request, pk):
    from .models import Almacen
    from .forms import AlmacenForm
    almacen = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        form = AlmacenForm(request.POST, instance=almacen)
        if form.is_valid():
            form.save()
            return redirect('logistica:almacen_list')
    else:
        form = AlmacenForm(instance=almacen)
    return render(request, 'logistica/almacen_form.html', {
        'titulo': 'Editar Almacén',
        'form': form
    })


@login_required
def reporte_stock(request):
    try:
        from apps.logistica.models import ExistenciaAlmacen
        from apps.produccion.models import MateriaPrima, ProductoTerminado
        existencias = ExistenciaAlmacen.objects.select_related('almacen').all()
        materias_primas = MateriaPrima.objects.filter(activo=True).order_by('nombre')
        productos_terminados = ProductoTerminado.objects.filter(activo=True).order_by('nombre')
    except Exception:
        existencias = []
        materias_primas = []
        productos_terminados = []
    return render(request, 'logistica/reporte_stock.html', {
        'titulo': 'Reporte de Existencias',
        'existencias': existencias,
        'materias_primas': materias_primas,
        'productos_terminados': productos_terminados,
    })


@login_required
def reporte_kardex(request):
    from datetime import datetime, time
    from apps.logistica.models import MovimientoInventario, RepuestoMaquina
    from apps.produccion.models import MateriaPrima, ProductoTerminado

    tipo_item = request.GET.get('tipo_item', 'MP')
    item_id = request.GET.get('item_id')
    movimientos = MovimientoInventario.objects.select_related(
        'materia_prima', 'producto_pt', 'repuesto',
        'almacen_origen', 'almacen_destino',
    ).order_by('fecha')
    item = None
    if tipo_item == 'PT':
        items = ProductoTerminado.objects.filter(activo=True).order_by('nombre')
        if item_id:
            item = items.filter(pk=item_id).first()
            movimientos = movimientos.filter(producto_pt=item) if item else movimientos.none()
    elif tipo_item == 'REP':
        items = RepuestoMaquina.objects.filter(activo=True).order_by('nombre')
        if item_id:
            item = items.filter(pk=item_id).first()
            movimientos = movimientos.filter(repuesto=item) if item else movimientos.none()
    else:
        tipo_item = 'MP'
        items = MateriaPrima.objects.filter(activo=True).order_by('nombre')
        if item_id:
            item = items.filter(pk=item_id).first()
            movimientos = movimientos.filter(materia_prima=item) if item else movimientos.none()

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    if fecha_desde:
        movimientos = movimientos.filter(fecha__gte=datetime.combine(
            datetime.strptime(fecha_desde, '%Y-%m-%d').date(), time.min
        ))
    if fecha_hasta:
        movimientos = movimientos.filter(fecha__lte=datetime.combine(
            datetime.strptime(fecha_hasta, '%Y-%m-%d').date(), time.max
        ))
    return render(request, 'logistica/reporte_kardex.html', {
        'titulo': 'Reporte Kardex',
        'movimientos': movimientos,
        'items': items,
        'item': item,
        'tipo_item': tipo_item,
    })


@login_required
def transferencia_create(request):
    return render(request, 'logistica/transferencia_form.html', {
        'titulo': 'Nueva Transferencia entre Almacenes',
    })