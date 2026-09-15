from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    EjercicioPresupuestarioForm, ModificacionPresupuestariaForm,
    NormaPresupuestoForm, ObjetivoInstitucionalForm, PartidaPresupuestariaForm,
    PlanEstrategicoForm, UnidadPresupuestariaForm,
)
from .models import (
    EjercicioPresupuestario, ModificacionPresupuestaria, NormaPresupuesto,
    ObjetivoInstitucional, PartidaPresupuestaria, PlanEstrategico,
    UnidadPresupuestaria,
)

RESOURCES = {
    'planes': (PlanEstrategico, PlanEstrategicoForm, 'Planes estratégicos'),
    'objetivos': (ObjetivoInstitucional, ObjetivoInstitucionalForm, 'Objetivos institucionales'),
    'ejercicios': (EjercicioPresupuestario, EjercicioPresupuestarioForm, 'Ejercicios presupuestarios'),
    'unidades': (UnidadPresupuestaria, UnidadPresupuestariaForm, 'Unidades presupuestarias'),
    'partidas': (PartidaPresupuestaria, PartidaPresupuestariaForm, 'Partidas presupuestarias'),
    'modificaciones': (ModificacionPresupuestaria, ModificacionPresupuestariaForm, 'Modificaciones presupuestarias'),
    'normas': (NormaPresupuesto, NormaPresupuestoForm, 'Normativa de planificación y presupuesto'),
}


@login_required
def dashboard(request):
    return render(request, 'planificacion_presupuesto/dashboard.html', {
        'planes': PlanEstrategico.objects.filter(estado__in=['aprobado', 'vigente']).count(),
        'ejercicios': EjercicioPresupuestario.objects.filter(estado__in=['aprobado', 'ejecucion']).count(),
        'partidas': PartidaPresupuestaria.objects.count(),
        'modificaciones': ModificacionPresupuestaria.objects.filter(estado__in=['solicitada', 'aprobada']).count(),
    })


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'planificacion_presupuesto/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('planificacion_presupuesto:resource_list', resource=resource)
    return render(request, 'planificacion_presupuesto/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('planificacion_presupuesto:resource_list', resource=resource)
    return render(request, 'planificacion_presupuesto/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
