from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.produccion.models import OrdenProduccion
from .forms import AuditoriaCalidadForm
from .models import AuditoriaCalidad


@login_required
def dashboard(request):
    auditorias = AuditoriaCalidad.objects.select_related('orden', 'inspector').all()
    return render(request, 'calidad/dashboard.html', {
        'auditorias': auditorias[:30],
        'pendientes': auditorias.filter(estado__in=('en_revision', 'reproceso')).count(),
    })


@login_required
def auditoria_create(request, pk=None):
    orden = get_object_or_404(OrdenProduccion, pk=pk) if pk else None
    form = AuditoriaCalidadForm(request.POST or None, initial={'orden': orden})
    if request.method == 'POST' and form.is_valid():
        auditoria = form.save(commit=False)
        auditoria.inspector = request.user
        if auditoria.estado in ('aprobado', 'aprobado_observacion', 'cerrado'):
            auditoria.validado_por = request.user
            auditoria.fecha_validacion = timezone.localdate()
        auditoria.save()
        return redirect('calidad:dashboard')
    return render(request, 'calidad/form.html', {
        'form': form,
        'orden': orden,
        'titulo': 'Registrar auditoría de aseguramiento de la calidad',
    })


@login_required
def auditoria_detail(request, pk):
    auditoria = get_object_or_404(AuditoriaCalidad.objects.select_related('orden'), pk=pk)
    return render(request, 'calidad/detail.html', {'auditoria': auditoria})
