from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    DotacionEquipoForm, GuardiaForm, IncidenteSeguridadForm,
    InspeccionSSTForm, OrdenSalidaMaterialForm, PaseIngresoForm,
    PuestoSeguridadForm, RegistroAccesoForm, RondaSeguridadForm,
    TurnoGuardiaForm,
)
from .models import (
    DotacionEquipo, Guardia, IncidenteSeguridad, InspeccionSST,
    OrdenSalidaMaterial, PaseIngreso, PuestoSeguridad, RegistroAcceso,
    RondaSeguridad, TurnoGuardia,
)


RESOURCE_MAP = {
    'guardias': (Guardia, GuardiaForm, 'Guardias'),
    'puestos': (PuestoSeguridad, PuestoSeguridadForm, 'Puestos de seguridad'),
    'turnos': (TurnoGuardia, TurnoGuardiaForm, 'Turnos 24x72'),
    'dotaciones': (DotacionEquipo, DotacionEquipoForm, 'Dotaciones'),
    'pases': (PaseIngreso, PaseIngresoForm, 'Pases de ingreso'),
    'accesos': (RegistroAcceso, RegistroAccesoForm, 'Registros de acceso'),
    'ordenes-salida': (OrdenSalidaMaterial, OrdenSalidaMaterialForm, 'Órdenes de salida'),
    'rondas': (RondaSeguridad, RondaSeguridadForm, 'Rondas de seguridad'),
    'incidentes': (IncidenteSeguridad, IncidenteSeguridadForm, 'Incidentes'),
    'inspecciones': (InspeccionSST, InspeccionSSTForm, 'Inspecciones SST'),
}


@login_required
def dashboard(request):
    context = {
        'guardias': Guardia.objects.filter(estado='activo').count(),
        'turnos_hoy': TurnoGuardia.objects.filter(inicio__date=timezone.localdate()).count(),
        'pases_vigentes': PaseIngreso.objects.filter(estado='autorizado').count(),
        'incidentes_abiertos': IncidenteSeguridad.objects.exclude(estado='cerrado').count(),
        'ordenes_pendientes': OrdenSalidaMaterial.objects.filter(estado__in=['solicitada', 'autorizada']).count(),
        'inspecciones_pendientes': InspeccionSST.objects.filter(estado__in=['planificada', 'con_hallazgos']).count(),
    }
    return render(request, 'seguridad/dashboard.html', context)


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCE_MAP[resource]
    return render(request, 'seguridad/resource_list.html', {
        'titulo': title,
        'recurso': resource,
        'registros': model.objects.all()[:100],
        'form': form_class(),
    })


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCE_MAP[resource]
    form = form_class(request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        if hasattr(record, 'registrado_por'):
            record.registrado_por = request.user
        if hasattr(record, 'reportado_por'):
            record.reportado_por = request.user
        if hasattr(record, 'autorizado_por') and record.estado == 'autorizada':
            record.autorizado_por = request.user
        record.save()
        return redirect('seguridad:resource_list', resource=resource)
    return render(request, 'seguridad/resource_form.html', {'titulo': f'Nuevo {title}', 'form': form, 'recurso': resource})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCE_MAP[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, instance=record)
    if form.is_valid():
        updated = form.save(commit=False)
        if hasattr(updated, 'registrado_por') and not updated.registrado_por_id:
            updated.registrado_por = request.user
        if hasattr(updated, 'reportado_por') and not updated.reportado_por_id:
            updated.reportado_por = request.user
        updated.save()
        return redirect('seguridad:resource_list', resource=resource)
    return render(request, 'seguridad/resource_form.html', {'titulo': f'Editar {title}', 'form': form, 'recurso': resource})
