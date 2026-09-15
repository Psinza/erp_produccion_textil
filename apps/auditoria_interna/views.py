from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import AccionCorrectivaForm, HallazgoAuditoriaForm, NormaAuditoriaForm, PlanAuditoriaForm
from .models import AccionCorrectiva, HallazgoAuditoria, NormaAuditoria, PlanAuditoria

RESOURCES = {
    'planes': (PlanAuditoria, PlanAuditoriaForm, 'Planes de auditoría'),
    'hallazgos': (HallazgoAuditoria, HallazgoAuditoriaForm, 'Hallazgos'),
    'acciones': (AccionCorrectiva, AccionCorrectivaForm, 'Acciones correctivas'),
    'normas': (NormaAuditoria, NormaAuditoriaForm, 'Normas y referencias'),
}


@login_required
def dashboard(request):
    return render(request, 'auditoria_interna/dashboard.html', {
        'planes_activos': PlanAuditoria.objects.filter(estado__in=['aprobado', 'en_ejecucion']).count(),
        'hallazgos_abiertos': HallazgoAuditoria.objects.exclude(estado='cerrado').count(),
        'acciones_vencidas': AccionCorrectiva.objects.filter(verificada=False, fecha_compromiso__lt=timezone.localdate()).count(),
    })


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'auditoria_interna/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('auditoria_interna:resource_list', resource=resource)
    return render(request, 'auditoria_interna/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('auditoria_interna:resource_list', resource=resource)
    return render(request, 'auditoria_interna/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
