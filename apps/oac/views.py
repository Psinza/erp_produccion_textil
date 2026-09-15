from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BusquedaMedicamentoForm, CitaCiudadanaForm, DonacionForm, JornadaMedicaForm, PersonalOACForm, PresupuestoOACForm
from .models import BusquedaMedicamento, CitaCiudadana, Donacion, JornadaMedica, PersonalOAC, PresupuestoOAC

RESOURCES = {
    'personal': (PersonalOAC, PersonalOACForm, 'Personal de la OAC'),
    'presupuestos': (PresupuestoOAC, PresupuestoOACForm, 'Presupuesto de la OAC'),
    'donaciones': (Donacion, DonacionForm, 'Donaciones'),
    'citas': (CitaCiudadana, CitaCiudadanaForm, 'Gestor de citas'),
    'busqueda-medicamentos': (BusquedaMedicamento, BusquedaMedicamentoForm, 'Búsqueda de medicamentos'),
    'jornadas-medicas': (JornadaMedica, JornadaMedicaForm, 'Jornadas médicas'),
}


@login_required
def dashboard(request):
    return render(request, 'oac/dashboard.html', {
        'donaciones_pendientes': Donacion.objects.filter(estado__in=['solicitada', 'aprobada']).count(),
        'citas_hoy': CitaCiudadana.objects.filter(fecha_cita__date=timezone.localdate()).exclude(estado='cancelada').count(),
        'medicamentos_abiertos': BusquedaMedicamento.objects.exclude(estado__in=['cerrada', 'no_disponible']).count(),
        'jornadas_proximas': JornadaMedica.objects.filter(fecha__gte=timezone.localdate()).exclude(estado='cancelada').count(),
        'ejecutado': sum((p.monto_ejecutado for p in PresupuestoOAC.objects.all()), 0),
    })


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'oac/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('oac:resource_list', resource=resource)
    return render(request, 'oac/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('oac:resource_list', resource=resource)
    return render(request, 'oac/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
