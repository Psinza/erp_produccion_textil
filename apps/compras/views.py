from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.facturacion.models import Proveedor
from apps.produccion.models import MateriaPrima
from .models import ProductoCompra, RequerimientoMaterial, DetalleRequerimientoMaterial
from .models import RecepcionCompra, DetalleRecepcionCompra
from .forms import (
    ProveedorForm, MateriaPrimaForm, ProductoCompraForm,
    RequerimientoMaterialForm, DetalleRequerimientoMaterialForm,
    RecepcionCompraForm, DetalleRecepcionCompraForm,
)

RequerimientoDetalleFormSet = inlineformset_factory(
    RequerimientoMaterial,
    DetalleRequerimientoMaterial,
    form=DetalleRequerimientoMaterialForm,
    extra=1,
    can_delete=True,
)

RecepcionDetalleFormSet = inlineformset_factory(
    RecepcionCompra,
    DetalleRecepcionCompra,
    form=DetalleRecepcionCompraForm,
    extra=1,
    can_delete=True,
)

@login_required
def dashboard(request):
    """Panel principal del módulo de Compras."""
    stats = {
        'ordenes_pendientes': 4,
        'compras_mes': 9420.00,
    }
    return render(request, 'compras/dashboard.html', {'titulo': 'Gestión de Compras', 'stats': stats})

# --- PROVEEDORES ---
@login_required
def proveedor_list(request):
    proveedores = Proveedor.objects.all().order_by('razon_social')
    return render(request, 'compras/proveedor_list.html', {'proveedores': proveedores, 'titulo': 'Proveedores'})

@login_required
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compras:proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'compras/proveedor_form.html', {'form': form, 'titulo': 'Nuevo Proveedor'})

@login_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('compras:proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'compras/proveedor_form.html', {'form': form, 'titulo': 'Editar Proveedor'})

# --- MATERIAS PRIMAS ---
@login_required
def materia_prima_list(request):
    materias = MateriaPrima.objects.all().order_by('nombre')
    return render(request, 'compras/materia_prima_list.html', {'materias': materias, 'titulo': 'Materias Primas'})

@login_required
def materia_prima_create(request):
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compras:materia_prima_list')
    else:
        form = MateriaPrimaForm()
    return render(request, 'compras/materia_prima_form.html', {'form': form, 'titulo': 'Nueva Materia Prima'})

@login_required
def materia_prima_update(request, pk):
    materia = get_object_or_404(MateriaPrima, pk=pk)
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('compras:materia_prima_list')
    else:
        form = MateriaPrimaForm(instance=materia)
    return render(request, 'compras/materia_prima_form.html', {'form': form, 'titulo': 'Editar Materia Prima'})

# --- PRODUCTOS DE COMPRA ---
@login_required
def producto_list(request):
    productos = ProductoCompra.objects.all().order_by('nombre')
    return render(request, 'compras/producto_list.html', {'productos': productos, 'titulo': 'Productos de Compra'})

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoCompraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compras:producto_list')
    else:
        form = ProductoCompraForm()
    return render(request, 'compras/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto de Compra'})

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(ProductoCompra, pk=pk)
    if request.method == 'POST':
        form = ProductoCompraForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('compras:producto_list')
    else:
        form = ProductoCompraForm(instance=producto)
    return render(request, 'compras/producto_form.html', {'form': form, 'titulo': 'Editar Producto de Compra'})


@login_required
def requerimiento_list(request):
    requerimientos = RequerimientoMaterial.objects.select_related('orden_produccion').order_by('-creado_en')
    return render(request, 'compras/requerimiento_list.html', {
        'requerimientos': requerimientos,
        'titulo': 'Requerimientos de materiales textiles',
    })


@login_required
def requerimiento_create(request):
    form = RequerimientoMaterialForm(request.POST or None)
    formset = RequerimientoDetalleFormSet(request.POST or None)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            requerimiento = form.save(commit=False)
            requerimiento.solicitado_por = request.user
            requerimiento.save()
            formset.instance = requerimiento
            formset.save()
        return redirect('compras:requerimiento_list')
    return render(request, 'compras/requerimiento_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Nuevo requerimiento de materiales',
    })


@login_required
def recepcion_create(request):
    form = RecepcionCompraForm(request.POST or None)
    formset = RecepcionDetalleFormSet(request.POST or None)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            recepcion = form.save(commit=False)
            requerimiento = getattr(recepcion.orden, 'requerimiento', None)
            if requerimiento and requerimiento.almacen_destino:
                recepcion.almacen = requerimiento.almacen_destino
            recepcion.recibido_por = request.user
            recepcion.save()
            formset.instance = recepcion
            formset.save()
        return redirect('compras:recepcion_list')
    return render(request, 'compras/recepcion_form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Recepción de materiales por orden de compra',
    })


@login_required
def recepcion_list(request):
    recepciones = RecepcionCompra.objects.select_related('orden', 'almacen').order_by('-fecha')
    return render(request, 'compras/recepcion_list.html', {
        'recepciones': recepciones,
        'titulo': 'Recepciones de compras',
    })