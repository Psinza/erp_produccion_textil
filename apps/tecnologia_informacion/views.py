from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AsignacionDiariaForm, EquipoTIForm, IndicadorGestionForm,
    MantenimientoEquipoForm, MonitoreoRedForm, PersonalTIForm,
    PlanModernizacionForm, PlanTrabajoTIForm, RecepcionEquipoForm,
    ServicioTIForm, SolicitudEquipoForm, TicketTIForm,
)
from .models import (
    AsignacionDiaria, EquipoTI, IndicadorGestion, MantenimientoEquipo,
    MonitoreoRed, PersonalTI, PlanModernizacion, PlanTrabajoTI,
    RecepcionEquipo, ServicioTI, SolicitudEquipo, TicketTI,
)


RESOURCES = {
    'personal': (PersonalTI, PersonalTIForm, 'Personal de tecnología'),
    'tickets': (TicketTI, TicketTIForm, 'Gestor de tickets'),
    'monitoreos': (MonitoreoRed, MonitoreoRedForm, 'Monitoreos de red'),
    'asignaciones': (AsignacionDiaria, AsignacionDiariaForm, 'Asignaciones diarias'),
    'equipos': (EquipoTI, EquipoTIForm, 'Inventario de equipos'),
    'mantenimientos': (MantenimientoEquipo, MantenimientoEquipoForm, 'Mantenimiento de equipos'),
    'planes-trabajo': (PlanTrabajoTI, PlanTrabajoTIForm, 'Planes de trabajo'),
    'solicitudes-equipos': (SolicitudEquipo, SolicitudEquipoForm, 'Solicitudes de equipos'),
    'recepciones': (RecepcionEquipo, RecepcionEquipoForm, 'Recepción de equipos'),
    'indicadores': (IndicadorGestion, IndicadorGestionForm, 'Indicadores de gestión'),
    'servicios': (ServicioTI, ServicioTIForm, 'Servicios tecnológicos'),
    'modernizacion': (PlanModernizacion, PlanModernizacionForm, 'Plan de modernización'),
}


@login_required
def dashboard(request):
    return render(request, 'tecnologia_informacion/dashboard.html', {
        'personal': PersonalTI.objects.filter(estado='activo').count(),
        'tickets_abiertos': TicketTI.objects.exclude(estado__in=['resuelto', 'cerrado', 'cancelado']).count(),
        'tickets_criticos': TicketTI.objects.filter(prioridad='critica').exclude(estado__in=['resuelto', 'cerrado', 'cancelado']).count(),
        'red_alertas': MonitoreoRed.objects.exclude(estado='operativo').count(),
        'equipos': EquipoTI.objects.exclude(estado='baja').count(),
        'equipos_mantenimiento': EquipoTI.objects.filter(estado='mantenimiento').count(),
        'servicios_activos': ServicioTI.objects.filter(estado='activo').count(),
        'servicios_apagados': ServicioTI.objects.filter(estado='apagado').count(),
        'asignaciones_hoy': AsignacionDiaria.objects.filter(fecha=timezone.localdate()).exclude(estado='completada').count(),
        'modernizaciones': PlanModernizacion.objects.filter(estado__in=['aprobado', 'en_ejecucion']).count(),
    })


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'tecnologia_informacion/resource_list.html', {
        'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100],
    })


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('tecnologia_informacion:resource_list', resource=resource)
    return render(request, 'tecnologia_informacion/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('tecnologia_informacion:resource_list', resource=resource)
    return render(request, 'tecnologia_informacion/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
