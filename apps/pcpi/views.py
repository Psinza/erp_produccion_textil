from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.produccion.models import OrdenProduccion, OrdenTrabajoProduccion
from .forms import (
    PlanificacionEntregaForm, ProgramacionSemanalForm,
    ResumenRequerimientosMaterialesForm, DistribucionOrdenTrabajoForm,
)
from .models import (
    PlanificacionEntrega, ProgramacionSemanal,
    ResumenRequerimientosMateriales, DistribucionOrdenTrabajo,
)


@login_required
def dashboard(request):
    return render(request, 'pcpi/dashboard.html', {
        'planificaciones': PlanificacionEntrega.objects.select_related('orden').order_by('-creado_en')[:10],
        'programaciones': ProgramacionSemanal.objects.select_related('planificacion__orden').order_by('-creado_en')[:10],
        'resumenes': ResumenRequerimientosMateriales.objects.select_related('orden').order_by('-creado_en')[:10],
    })


def _form_view(request, form_class, template_title, instance=None):
    form = form_class(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        if hasattr(obj, 'responsable'):
            obj.responsable = request.user
        if hasattr(obj, 'elaborado_por'):
            obj.elaborado_por = request.user
        obj.save()
        return redirect('pcpi:dashboard')
    return render(request, 'pcpi/form.html', {'form': form, 'titulo': template_title})


@login_required
def planificacion_create(request):
    return _form_view(request, PlanificacionEntregaForm, 'Planificación de fechas de entrega', None)


@login_required
def planificacion_update(request, pk):
    item = get_object_or_404(PlanificacionEntrega, pk=pk)
    return _form_view(request, PlanificacionEntregaForm, 'Editar planificación de fechas de entrega', item)


@login_required
def programacion_create(request):
    return _form_view(request, ProgramacionSemanalForm, 'Programación semanal PCPI', None)


@login_required
def programacion_update(request, pk):
    item = get_object_or_404(ProgramacionSemanal, pk=pk)
    return _form_view(request, ProgramacionSemanalForm, 'Editar programación semanal PCPI', item)


@login_required
def resumen_create(request):
    return _form_view(request, ResumenRequerimientosMaterialesForm, 'Resumen de requerimientos de materiales', None)


@login_required
def resumen_update(request, pk):
    item = get_object_or_404(ResumenRequerimientosMateriales, pk=pk)
    return _form_view(request, ResumenRequerimientosMaterialesForm, 'Editar resumen de requerimientos de materiales', item)


@login_required
def distribucion_create(request, pk):
    orden_trabajo = get_object_or_404(OrdenTrabajoProduccion, pk=pk)
    form = DistribucionOrdenTrabajoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        distribucion = form.save(commit=False)
        distribucion.orden_trabajo = orden_trabajo
        distribucion.recibido_por = request.user if distribucion.recibido else None
        distribucion.save()
        return redirect('pcpi:dashboard')
    return render(request, 'pcpi/form.html', {
        'form': form,
        'titulo': f'Distribuir orden de trabajo {orden_trabajo.numero}',
    })
