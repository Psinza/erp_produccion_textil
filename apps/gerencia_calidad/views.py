from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AuditoriaCalidadISOForm, IndicadorCalidadForm, NoConformidadForm, NormaCalidadForm, ProcesoCalidadForm
from .models import AuditoriaCalidadISO, IndicadorCalidad, NoConformidad, NormaCalidad, ProcesoCalidad

RESOURCES = {'normas': (NormaCalidad, NormaCalidadForm, 'Normas ISO y referencias'), 'procesos': (ProcesoCalidad, ProcesoCalidadForm, 'Procesos de calidad'), 'auditorias': (AuditoriaCalidadISO, AuditoriaCalidadISOForm, 'Auditorías ISO'), 'no-conformidades': (NoConformidad, NoConformidadForm, 'No conformidades'), 'indicadores': (IndicadorCalidad, IndicadorCalidadForm, 'Indicadores de calidad')}

@login_required
def dashboard(request):
    return render(request, 'gerencia_calidad/dashboard.html', {'auditorias_activas': AuditoriaCalidadISO.objects.exclude(estado='cerrada').count(), 'no_conformidades_abiertas': NoConformidad.objects.exclude(estado='cerrada').count(), 'procesos_activos': ProcesoCalidad.objects.filter(activo=True).count()})

@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'gerencia_calidad/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})

@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('gerencia_calidad:resource_list', resource=resource)
    return render(request, 'gerencia_calidad/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})

@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('gerencia_calidad:resource_list', resource=resource)
    return render(request, 'gerencia_calidad/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
