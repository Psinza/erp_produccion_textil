from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ContratoForm, EvaluacionContratacionForm, NormaContratacionForm,
    OfertaProveedorForm, ProcesoContratacionForm, ProveedorForm,
)
from .models import (
    Contrato, EvaluacionContratacion, NormaContratacion, OfertaProveedor,
    ProcesoContratacion, Proveedor,
)

RESOURCES = {
    'proveedores': (Proveedor, ProveedorForm, 'Registro de proveedores'),
    'procesos': (ProcesoContratacion, ProcesoContratacionForm, 'Procesos de contratación'),
    'ofertas': (OfertaProveedor, OfertaProveedorForm, 'Ofertas recibidas'),
    'evaluaciones': (EvaluacionContratacion, EvaluacionContratacionForm, 'Evaluaciones'),
    'contratos': (Contrato, ContratoForm, 'Contratos'),
    'normas': (NormaContratacion, NormaContratacionForm, 'Normativa de contrataciones'),
}


@login_required
def dashboard(request):
    return render(request, 'contrataciones_publicas/dashboard.html', {
        'procesos': ProcesoContratacion.objects.exclude(estado__in=['cerrado', 'anulado']).count(),
        'ofertas': OfertaProveedor.objects.filter(estado='recibida').count(),
        'contratos': Contrato.objects.filter(estado='vigente').count(),
        'proveedores': Proveedor.objects.filter(estado='activo').count(),
    })


@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'contrataciones_publicas/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})


@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('contrataciones_publicas:resource_list', resource=resource)
    return render(request, 'contrataciones_publicas/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})


@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('contrataciones_publicas:resource_list', resource=resource)
    return render(request, 'contrataciones_publicas/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
