from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    EquipoServiciosForm, PersonalServiciosForm, PlanMantenimientoForm,
    SolicitudMaterialForm, SolicitudServicioForm, TareaDiariaForm,
    UbicacionForm,
)
from .models import (
    EquipoServicios, PersonalServicios, PlanMantenimiento, SolicitudMaterial,
    SolicitudServicio, TareaDiaria, Ubicacion,
)


RESOURCES = {
    'ubicaciones': (Ubicacion, UbicacionForm, 'Ubicaciones'),
    'personal': (PersonalServicios, PersonalServiciosForm, 'Personal de servicios generales'),
    'tareas': (TareaDiaria, TareaDiariaForm, 'Tareas diarias'),
    'mantenimientos': (PlanMantenimiento, PlanMantenimientoForm, 'Mantenimientos'),
    'equipos': (EquipoServicios, EquipoServiciosForm, 'Inventario de equipos'),
    'solicitudes-material': (SolicitudMaterial, SolicitudMaterialForm, 'Solicitudes de material'),
    'solicitudes-servicio': (SolicitudServicio, SolicitudServicioForm, 'Solicitudes de servicio'),
}


@login_required
def dashboard(request):
    return render(request, 'servicios_generales/dashboard.html', {
        'personal': PersonalServicios.objects.filter(estado='activo').count(),
        'tareas_pendientes': TareaDiaria.objects.filter(fecha=timezone.localdate()).exclude(estado='completada').count(),
        'mantenimientos_abiertos': PlanMantenimiento.objects.exclude(estado__in=['completado', 'cancelado']).count(),
        'equipos_operativos': EquipoServicios.objects.filter(estado='operativo').count(),
        'materiales_pendientes': SolicitudMaterial.objects.filter(estado__in=['solicitada', 'aprobada']).count(),
        'servicios_pendientes': SolicitudServicio.objects.filter(estado__in=['solicitada', 'aprobada', 'asignada', 'en_ejecucion']).count(),
    })


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'servicios_generales/resource_list.html', {
        'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100],
    })


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('servicios_generales:resource_list', resource=resource)
    return render(request, 'servicios_generales/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('servicios_generales:resource_list', resource=resource)
    return render(request, 'servicios_generales/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
