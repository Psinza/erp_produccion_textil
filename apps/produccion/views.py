from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import (
    OrdenProduccion, ProductoTerminado, DepartamentoUDP, 
    DepartamentoCorte, DepartamentoBordado, DepartamentoProduccion,
    DepartamentoDespacho, DepartamentoCalidadISO9001,
    ProcesoDepartamento, IndicadorProceso, MedicionIndicador,
    Notificacion, NoConformidad,
)
from .forms import (
    OrdenProduccionForm, DepartamentoUDPForm, DepartamentoCorteForm,
    DepartamentoBordadoForm, DepartamentoProduccionForm, DepartamentoDespachoForm,
    DepartamentoCalidadISOForm, ProcesoDepartamentoForm,
    MedicionIndicadorForm, NoConformidadForm,
)
from .mecanica import (
    ChequeoLineaForm, LineaProduccionForm, MaquinaTextilForm,
    OrdenMantenimientoForm, PlanMantenimientoForm, SolicitudPiezaForm,
)
from .models import (
    ChequeoLineaProduccion, LineaProduccion, MaquinaTextil,
    OrdenMantenimientoTextil, PlanMantenimientoTextil, SolicitudPiezaMecanica,
)


def _notificar(orden, mensaje, tipo='flujo'):
    usuario = orden.responsable or get_user_model().objects.filter(is_staff=True, is_active=True).first()
    if usuario:
        Notificacion.objects.create(
            orden=orden,
            destinatario=usuario,
            tipo=tipo,
            mensaje=mensaje,
        )


def _registrar_rechazo(orden, cantidad, origen):
    if not cantidad:
        return
    total = max(orden.cantidad_a_producir, 1)
    porcentaje = round(cantidad * 100 / total, 2)
    if porcentaje >= 5:
        NoConformidad.objects.create(
            orden=orden,
            origen=origen,
            descripcion=f'Rechazo superior al umbral en {origen}.',
            cantidad_afectada=cantidad,
            porcentaje_rechazo=porcentaje,
            accion_inmediata='Retener lote para análisis del Pool de calidad.',
            responsable=orden.responsable,
        )
        _notificar(orden, f'No conformidad abierta por rechazo de {porcentaje}%.', 'calidad')

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
        'mecanica_maquinas': MaquinaTextil.objects.filter(activa=True).count(),
        'mecanica_pendientes': OrdenMantenimientoTextil.objects.filter(estado__in=['planificada', 'en_proceso']).count(),
    })


@login_required
def mecanica_dashboard(request):
    return render(request, 'produccion/mecanica_dashboard.html', {
        'maquinas': MaquinaTextil.objects.select_related('linea').filter(activa=True),
        'lineas': LineaProduccion.objects.filter(activa=True),
        'mantenimientos': OrdenMantenimientoTextil.objects.select_related('maquina').exclude(estado='completada').order_by('fecha_programada')[:10],
        'solicitudes': SolicitudPiezaMecanica.objects.select_related('maquina', 'pieza').filter(estado='pendiente').prefetch_related('requerimientos_compra')[:10],
        'chequeos': ChequeoLineaProduccion.objects.select_related('linea').order_by('-fecha')[:5],
    })


def _mecanica_form(request, form_class, template, title, redirect_name, instance=None):
    form = form_class(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        if hasattr(obj, 'responsable_id') and not obj.responsable_id:
            obj.responsable = request.user
        if hasattr(obj, 'solicitante_id') and not obj.solicitante_id:
            obj.solicitante = request.user
        obj.save()
        return redirect(redirect_name)
    return render(request, template, {'form': form, 'titulo': title})


@login_required
def mecanica_maquina_create(request):
    return _mecanica_form(request, MaquinaTextilForm, 'produccion/mecanica_form.html', 'Nueva Máquina Textil', 'produccion:mecanica_dashboard')


@login_required
def mecanica_linea_create(request):
    return _mecanica_form(request, LineaProduccionForm, 'produccion/mecanica_form.html', 'Nueva Línea de Producción', 'produccion:mecanica_dashboard')


@login_required
def mecanica_solicitud_create(request):
    form = SolicitudPiezaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        from apps.compras.models import RequerimientoMaterial, DetalleRequerimientoMaterial
        from apps.logistica.models import Almacen, RepuestoMaquina
        from django.db import transaction

        with transaction.atomic():
            solicitud = form.save(commit=False)
            solicitud.solicitante = request.user
            solicitud.save()

            repuesto = solicitud.pieza
            if not repuesto:
                codigo = f'MEC-{solicitud.pk:06d}'
                repuesto = RepuestoMaquina.objects.create(
                    codigo=codigo,
                    nombre=solicitud.pieza_nueva.strip(),
                    tipo='otro',
                    maquina_compatible=solicitud.maquina.nombre,
                    unidad_medida='unidad',
                    activo=True,
                )
                solicitud.pieza = repuesto
                solicitud.save(update_fields=['pieza'])

            almacen = Almacen.objects.filter(
                tipo='repuestos', activo=True
            ).order_by('-es_principal', 'id').first()
            if not almacen:
                almacen = Almacen.objects.create(
                    nombre='Almacén de Repuestos de Máquinas',
                    tipo='repuestos',
                    ubicacion='Mantenimiento de confección',
                    activo=True,
                )

            numero = f'MEC-{solicitud.pk:06d}'
            requerimiento = RequerimientoMaterial.objects.create(
                numero=numero,
                solicitud_pieza=solicitud,
                almacen_destino=almacen,
                solicitado_por=request.user,
                estado='borrador',
                fecha_requerida=timezone.localdate(),
                observaciones=(
                    f'Solicitud de Mecánica Industrial Textil para la máquina '
                    f'{solicitud.maquina.codigo}. Prioridad: {solicitud.get_prioridad_display()}.'
                ),
            )
            DetalleRequerimientoMaterial.objects.create(
                requerimiento=requerimiento,
                repuesto=repuesto,
                descripcion=repuesto.nombre,
                cantidad=solicitud.cantidad,
                unidad_medida=repuesto.unidad_medida,
                especificacion=solicitud.especificacion_pieza,
            )
        return redirect('produccion:mecanica_dashboard')
    return render(request, 'produccion/mecanica_form.html', {
        'form': form,
        'titulo': 'Solicitar Pieza de Máquina',
    })


@login_required
def mecanica_mantenimiento_create(request):
    return _mecanica_form(request, OrdenMantenimientoForm, 'produccion/mecanica_form.html', 'Nueva Orden de Mantenimiento', 'produccion:mecanica_dashboard')


@login_required
def mecanica_chequeo_create(request):
    return _mecanica_form(request, ChequeoLineaForm, 'produccion/mecanica_form.html', 'Nuevo Chequeo de Línea', 'produccion:mecanica_dashboard')


@login_required
def mecanica_plan_create(request):
    return _mecanica_form(request, PlanMantenimientoForm, 'produccion/mecanica_form.html', 'Nuevo Plan de Mantenimiento', 'produccion:mecanica_dashboard')

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
            _notificar(orden, 'Nueva orden creada y pendiente de definición UDP.')
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
            if udp.aprobado:
                from .services import generar_requerimiento_desde_ficha
                requerimiento = generar_requerimiento_desde_ficha(orden, request.user)
                orden.estado = 'en_corte'
                orden.save()
                mensaje = 'UDP completó la ficha técnica.'
                if requerimiento:
                    mensaje += f' Requerimiento {requerimiento.numero} generado para Logística.'
                _notificar(orden, mensaje)
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
            if corte_obj.corte_habilitado:
                orden.estado = 'en_bordado'
                orden.save()
                _registrar_rechazo(orden, corte_obj.piezas_defectuosas_corte, 'corte')
                _notificar(orden, 'Corte habilitado y enviado a Bordados.')
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
            _registrar_rechazo(orden, bordado.piezas_rechazadas_bordado, 'bordados')
            _notificar(orden, 'Bordados registrados y lote enviado a Producción textil.')
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
            _registrar_rechazo(orden, p_obj.piezas_con_falla_costura, 'produccion_textil')
            _notificar(orden, 'Producción textil registrada y lote enviado a Despacho.')
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
            
            if d_obj.planchado_ok and d_obj.empaquetado_ok and d_obj.fibras_hilos_sueltos_ok:
                orden.estado = 'en_calidad'
                orden.save()
                _notificar(orden, 'Despacho completó planchado, revisión y empaque. Pendiente Pool.')
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
            _registrar_rechazo(orden, c_obj.piezas_rechazadas_qc, 'pool')
            _notificar(orden, 'Pool de calidad registró el dictamen del lote.', 'calidad')
            return redirect('produccion:orden_detail', pk=pk)
    else:
        form = DepartamentoCalidadISOForm(instance=calidad)
    return render(request, 'produccion/depto_form.html', {'titulo': 'Control de Calidad ISO 9001 y Notificación Directiva', 'form': form, 'orden': orden})

@login_required
def producto_terminado_list(request):
    productos = ProductoTerminado.objects.all()
    return render(request, 'produccion/producto_terminado_list.html', {'titulo': 'Catálogo de Prendas y Productos', 'productos': productos})


@login_required
def proceso_list(request):
    procesos = ProcesoDepartamento.objects.select_related('orden').all()
    return render(request, 'produccion/proceso_list.html', {'procesos': procesos, 'titulo': 'Planes de procesos ISO'})


@login_required
def proceso_create(request, pk):
    orden = get_object_or_404(OrdenProduccion, pk=pk)
    form = ProcesoDepartamentoForm(request.POST or None, initial={'orden': orden})
    if request.method == 'POST' and form.is_valid():
        proceso = form.save(commit=False)
        proceso.orden = orden
        proceso.save()
        messages.success(request, 'Plan de proceso registrado.')
        return redirect('produccion:proceso_list')
    return render(request, 'produccion/depto_form.html', {'titulo': 'Plan de proceso ISO', 'form': form, 'orden': orden})


@login_required
def indicador_dashboard(request):
    indicadores = IndicadorProceso.objects.filter(activo=True).prefetch_related('mediciones')
    return render(request, 'produccion/indicador_dashboard.html', {'indicadores': indicadores, 'titulo': 'Indicadores de producción'})


@login_required
def indicador_medicion_create(request):
    form = MedicionIndicadorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        medicion = form.save(commit=False)
        medicion.registrado_por = request.user
        medicion.save()
        return redirect('produccion:indicador_dashboard')
    return render(request, 'produccion/indicador_medicion_form.html', {'form': form, 'titulo': 'Registrar medición'})


@login_required
def notificacion_list(request):
    notificaciones = Notificacion.objects.filter(destinatario=request.user)
    notificaciones.filter(leida=False).update(leida=True)
    return render(request, 'produccion/notificacion_list.html', {'notificaciones': notificaciones, 'titulo': 'Notificaciones de producción'})


@login_required
def no_conformidad_list(request):
    no_conformidades = NoConformidad.objects.select_related('orden', 'responsable').all()
    return render(request, 'produccion/no_conformidad_list.html', {'no_conformidades': no_conformidades, 'titulo': 'No conformidades'})


@login_required
def no_conformidad_create(request, pk=None):
    initial = {'orden': pk} if pk else None
    form = NoConformidadForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        no_conformidad = form.save(commit=False)
        no_conformidad.responsable = no_conformidad.responsable or request.user
        no_conformidad.save()
        _notificar(no_conformidad.orden, 'Se registró una no conformidad para revisión.', 'calidad')
        return redirect('produccion:no_conformidad_list')
    return render(request, 'produccion/no_conformidad_detail.html', {'form': form, 'titulo': 'Registrar no conformidad'})