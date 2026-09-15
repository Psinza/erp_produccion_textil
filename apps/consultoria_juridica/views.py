from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CasoJuridicoForm, ContratoJuridicoForm, DictamenJuridicoForm, NormaLegalForm
from .models import CasoJuridico, ContratoJuridico, DictamenJuridico, NormaLegal

RESOURCES = {'casos': (CasoJuridico, CasoJuridicoForm, 'Casos jurídicos'), 'dictamenes': (DictamenJuridico, DictamenJuridicoForm, 'Dictámenes'), 'normas': (NormaLegal, NormaLegalForm, 'Normativa legal'), 'contratos': (ContratoJuridico, ContratoJuridicoForm, 'Contratos jurídicos')}

@login_required
def dashboard(request):
    return render(request, 'consultoria_juridica/dashboard.html', {
        'casos_abiertos': CasoJuridico.objects.exclude(estado__in=['cerrado', 'archivado']).count(),
        'contratos_vigentes': ContratoJuridico.objects.filter(estado='vigente').count(),
        'dictamenes_pendientes': DictamenJuridico.objects.filter(aprobado=False).count(),
    })

@login_required
def resource_list(request, resource):
    model, form_class, title = RESOURCES[resource]
    return render(request, 'consultoria_juridica/resource_list.html', {'titulo': title, 'recurso': resource, 'registros': model.objects.all()[:100]})

@login_required
def resource_create(request, resource):
    model, form_class, title = RESOURCES[resource]
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('consultoria_juridica:resource_list', resource=resource)
    return render(request, 'consultoria_juridica/resource_form.html', {'titulo': f'Nuevo registro - {title}', 'form': form})

@login_required
def resource_update(request, resource, pk):
    model, form_class, title = RESOURCES[resource]
    record = get_object_or_404(model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('consultoria_juridica:resource_list', resource=resource)
    return render(request, 'consultoria_juridica/resource_form.html', {'titulo': f'Editar registro - {title}', 'form': form})
