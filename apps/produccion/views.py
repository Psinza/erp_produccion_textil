from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    OrdenProduccion, ProductoTerminado, DepartamentoUDP, 
    DepartamentoCorte, DepartamentoBordado, DepartamentoProduccion, 
    DepartamentoDespacho, DepartamentoCalidadISO9001
)
from .forms import (
    OrdenProduccionForm, DepartamentoUDPForm, DepartamentoCorteForm,
    DepartamentoBordadoForm, DepartamentoProduccionForm, DepartamentoDespachoForm,
    DepartamentoCalidadISOForm
)

@login_required
def dashboard(request):
    """Panel principal con métricas para Gerencia y Directiva."""
    total_ordenes = OrdenProduccion.objects.count()
    activas = OrdenProduccion.objects.exclude(estado__in=['completada', 'anulada']).count()
    
    total_producidas = sum(o.piezas_producidas_ok for o in OrdenProduccion.objects.all())
    total_rechazadas = sum(o.piezas_rechazadas for o in OrdenProduccion.objects.all())

    stats = {
        'total_ordenes': total_ordenes,
        'activas': activas,
        'total_producidas': total_producidas,
        'total_rechazadas': total_rechazadas,
        'udp_count': OrdenProduccion.objects.filter(estado='planificada').count(),
        'corte_count': OrdenProduccion.objects.filter(estado='en_corte').count(),
        'bordado_count': OrdenProduccion.objects.filter(estado='en_bordado').count(),
        'produccion_count': OrdenProduccion.objects.filter(estado='en_produccion').count(),
        'despacho_count': OrdenProduccion.objects.filter(estado='en_despacho').count(),
        'calidad_count': OrdenProduccion.objects.filter(estado='en_calidad').count(),
    }
    
    ordenes_recientes = OrdenProduccion.objects.select_related('producto').order_by('-id')[:6]

    return render(request, 'produccion/dashboard_produccion.html', {
        'titulo': 'Gerencia y Control de Producción Textil',
        'stats': stats,
        'ordenes_recientes': ordenes_recientes,
    })

@login_required
def orden_list(request):
    ordenes = OrdenProduccion.objects.all().order_by('-id')
    return render(request, 'produccion/orden_list.html', {'titulo': 'Órdenes de Producción Activas', 'ordenes': ordenes})

@login_required
def orden_create(request):
    if request.method == 'POST':
        form = OrdenProduccionForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.responsable = request.user
            orden.save()
            # Inicializar registro UDP por defecto
            DepartamentoUDP.objects.create(orden=orden, proyecto="Nuevo Proyecto", tipo_diseno="Estándar")
            return redirect('produccion:orden_detail', pk=orden.pk)
    else:
        form = OrdenProduccionForm()
    return render(request, 'produccion/orden_form.html', {'titulo': 'Nueva Orden de Producción', 'form': form})

@login_required
def orden_detail(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    return render(request, 'produccion/orden_detail.html', {'titulo': f'Detalle Lote: {orden.lote_numero}', 'orden': orden})

# --- VISTAS DE GESTIÓN POR DEPARTAMENTO ---

@login_required
def gestionar_udp(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    udp, _ = DepartamentoUDP.objects.get_or_create(orden=orden)
    if request.method == 'POST':
        form = DepartamentoUDPForm(request.POST, instance=udp)
        if form.is_valid():
            form.save()
            orden.estado = 'en_corte'
            orden.save()
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoUDPForm(instance=udp)
    return render(request, 'produccion/depto_form.html', {'titulo': 'Departamento UDP (Diseños y Pronted)', 'form': form, 'orden': orden})

@login_required
def gestionar_corte(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    corte, _ = DepartamentoCorte.objects.get_or_create(orden=orden)
    if request.method == 'POST':
        form = DepartamentoCorteForm(request.POST, instance=corte)
        if form.is_valid():
            corte_obj = form.save()
            orden.piezas_realizadas = corte_obj.piezas_por_lote
            orden.piezas_rechazadas += corte_obj.piezas_defectuosas_corte
            orden.estado = 'en_bordado'
            orden.save()
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoCorteForm(instance=corte)
    return render(request, 'produccion/depto_form.html', {'titulo': 'Departamento de Corte', 'form': form, 'orden': orden})

@login_required
def gestionar_bordado(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    if request.method == 'POST':
        form = DepartamentoBordadoForm(request.POST)
        if form.is_valid():
            bordado = form.save(commit=False)
            bordado.orden = orden
            bordado.operario = request.user
            bordado.save()
            
            orden.piezas_rechazadas += bordado.piezas_rechazadas_bordado
            orden.estado = 'en_produccion'
            orden.save()
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoBordadoForm()
    return render(request, 'produccion/depto_form.html', {'titulo': 'Departamento de Bordados (Logos / Nombres)', 'form': form, 'orden': orden})

@login_required
def gestionar_produccion(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    prod, _ = DepartamentoProduccion.objects.get_or_create(orden=orden)
    if request.method == 'POST':
        form = DepartamentoProduccionForm(request.POST, instance=prod)
        if form.is_valid():
            p_obj = form.save()
            orden.piezas_rechazadas += p_obj.piezas_con_falla_costura
            orden.estado = 'en_despacho'
            orden.save()
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoProduccionForm(instance=prod)
    return render(request, 'produccion/depto_form.html', {'titulo': 'Departamento de Producción / Confección', 'form': form, 'orden': orden})

@login_required
def gestionar_despacho(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    desp, _ = DepartamentoDespacho.objects.get_or_create(orden=orden)
    if request.method == 'POST':
        form = DepartamentoDespachoForm(request.POST, instance=desp)
        if form.is_valid():
            d_obj = form.save(commit=False)
            d_obj.responsable_empaque = request.user
            d_obj.save()
            
            orden.estado = 'en_calidad'
            orden.save()
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoDespachoForm(instance=desp)
    return render(request, 'produccion/depto_form.html', {'titulo': 'Departamento de Despacho (Planchado y Empaque)', 'form': form, 'orden': orden})

@login_required
def gestionar_calidad(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    calidad, _ = DepartamentoCalidadISO9001.objects.get_or_create(orden=orden)
    if request.method == 'POST':
        form = DepartamentoCalidadISOForm(request.POST, instance=calidad)
        if form.is_valid():
            c_obj = form.save(commit=False)
            c_obj.auditor = request.user
            c_obj.save()
            
            orden.piezas_producidas_ok = c_obj.piezas_aprobadas_qc
            orden.piezas_rechazadas += c_obj.piezas_rechazadas_qc
            if c_obj.cumple_iso_9001:
                orden.estado = 'completada'
            orden.save()
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoCalidadISOForm(instance=calidad)
    return render(request, 'produccion/depto_form.html', {'titulo': 'Control de Calidad ISO 9001 y Notificación Directiva', 'form': form, 'orden': orden})

@login_required
def producto_terminado_list(request):
    productos = ProductoTerminado.objects.all()
    return render(request, 'produccion/producto_terminado_list.html', {'titulo': 'Catálogo de Prendas y Productos', 'productos': productos})