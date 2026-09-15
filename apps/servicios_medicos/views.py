from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AfectacionPersonalForm, EquipoMedicoForm, PersonalMedicoForm, PresupuestoMedicoForm, ReposoMedicoForm, ResultadoIngresoForm
from .models import AfectacionPersonal, EquipoMedico, PersonalMedico, PresupuestoMedico, ReposoMedico, ResultadoIngreso

RESOURCES = {
    'personal': (PersonalMedico, PersonalMedicoForm, 'Personal médico'),
    'presupuestos': (PresupuestoMedico, PresupuestoMedicoForm, 'Presupuesto médico'),
    'resultados-ingreso': (ResultadoIngreso, ResultadoIngresoForm, 'Resultados de ingreso'),
    'reposos': (ReposoMedico, ReposoMedicoForm, 'Reposos médicos'),
    'afectaciones': (AfectacionPersonal, AfectacionPersonalForm, 'Afectaciones del personal'),
    'equipos': (EquipoMedico, EquipoMedicoForm, 'Dotación de equipos médicos'),
}

@login_required
def dashboard(request):
    return render(request, 'servicios_medicos/dashboard.html', {
        'ingresos_pendientes': ResultadoIngreso.objects.filter(estado='pendiente').count(),
        'reposos_abiertos': ReposoMedico.objects.filter(estado__in=['solicitado', 'validado']).count(),
        'afectaciones_abiertas': AfectacionPersonal.objects.exclude(estado='cerrada').count(),
        'equipos_operativos': EquipoMedico.objects.filter(estado='operativo').count(),
        'ejecutado': sum((p.monto_ejecutado for p in PresupuestoMedico.objects.all()), 0),
    })

@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'servicios_medicos/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})

@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('servicios_medicos:resource_list', resource=resource)
    return render(request, 'servicios_medicos/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})

@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('servicios_medicos:resource_list', resource=resource)
    return render(request, 'servicios_medicos/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
