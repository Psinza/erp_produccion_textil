from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import CategoriaComercial, InformacionComercial, ListaPrecio, ItemPrecio, OrdenProduccionComercial, EncuestaSatisfaccionCliente
from .forms import CategoriaComercialForm, InformacionComercialForm, ListaPrecioForm, ItemPrecioForm, OrdenProduccionComercialForm, EncuestaSatisfaccionClienteForm

@login_required
def dashboard_comercializacion(request):
    """Dashboard de comercialización."""
    categorias = CategoriaComercial.objects.all()
    productos = InformacionComercial.objects.select_related('producto', 'categoria').all()
    listas = ListaPrecio.objects.filter(activa=True)
    
    context = {
        'categorias': categorias,
        'productos': productos,
        'listas': listas,
        'total_productos_catalogo': productos.count(),
        'listas_activas': listas.count(),
        'productos_en_oferta': productos.filter(en_oferta=True).count(),
        'productos_destacados': productos.filter(destacado=True).count(),
        'ultimos_productos': productos.order_by('-id')[:5],
        'ordenes_produccion': OrdenProduccionComercial.objects.select_related('producto').all()[:5],
    }
    return render(request, 'comercializacion/dashboard.html', context)


@login_required
def orden_produccion_list(request):
    ordenes = OrdenProduccionComercial.objects.select_related('producto', 'orden_produccion')
    return render(request, 'comercializacion/orden_produccion_list.html', {'ordenes': ordenes})


@login_required
def orden_produccion_create(request):
    form = OrdenProduccionComercialForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        orden = form.save(commit=False)
        orden.creado_por = request.user
        orden.save()
        messages.success(request, 'Orden comercial guardada y editable.')
        return redirect('comercializacion:orden_produccion_detail', orden.pk)
    return render(request, 'comercializacion/orden_produccion_form.html', {'form': form, 'title': 'Nueva Orden de Producción Comercial'})


@login_required
def orden_produccion_update(request, pk):
    orden = get_object_or_404(OrdenProduccionComercial, pk=pk)
    form = OrdenProduccionComercialForm(request.POST or None, instance=orden)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Orden comercial actualizada.')
        return redirect('comercializacion:orden_produccion_detail', orden.pk)
    return render(request, 'comercializacion/orden_produccion_form.html', {'form': form, 'title': f'Editar {orden.numero}', 'orden': orden})


@login_required
def orden_produccion_detail(request, pk):
    orden = get_object_or_404(OrdenProduccionComercial.objects.select_related('producto', 'orden_produccion'), pk=pk)
    return render(request, 'comercializacion/orden_produccion_detail.html', {'orden': orden})


@login_required
def enviar_a_produccion(request, pk):
    orden = get_object_or_404(OrdenProduccionComercial, pk=pk)
    if request.method != 'POST':
        return redirect('comercializacion:orden_produccion_detail', pk)
    from apps.produccion.models import OrdenProduccion
    if orden.orden_produccion_id:
        messages.info(request, 'La orden ya fue enviada a Producción.')
    else:
        produccion = OrdenProduccion.objects.create(
            lote_numero=orden.numero,
            producto=orden.producto,
            cantidad_a_producir=orden.cantidad_total,
            fecha_planificada=orden.fecha_entrega,
            observaciones=orden.observaciones,
        )
        orden.orden_produccion = produccion
        orden.estado = 'enviada'
        orden.save(update_fields=['orden_produccion', 'estado', 'actualizado_en'])
        messages.success(request, 'Orden enviada a Producción para su ejecución.')
    return redirect('produccion:orden_detail', orden.orden_produccion_id)


@login_required
def encuesta_list(request):
    return render(request, 'comercializacion/encuesta_list.html', {
        'encuestas': EncuestaSatisfaccionCliente.objects.order_by('-fecha', '-creada_en'),
    })


@login_required
def encuesta_create(request, pk=None):
    instancia = get_object_or_404(EncuestaSatisfaccionCliente, pk=pk) if pk else None
    form = EncuestaSatisfaccionClienteForm(request.POST or None, instance=instancia)
    if request.method == 'POST' and form.is_valid():
        encuesta = form.save(commit=False)
        encuesta.registrada_por = request.user
        encuesta.save()
        return redirect('comercializacion:encuesta_list')
    return render(request, 'comercializacion/encuesta_form.html', {
        'form': form,
        'titulo': 'Editar encuesta de satisfacción' if instancia else 'Nueva encuesta de satisfacción',
    })

# Categorías
@login_required
def categoria_list(request):
    categorias = CategoriaComercial.objects.all()
    return render(request, 'comercializacion/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaComercialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('comercializacion:categoria_list')
    else:
        form = CategoriaComercialForm()
    return render(request, 'comercializacion/categoria_form.html', {'form': form, 'title': 'Crear Categoría'})

@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(CategoriaComercial, pk=pk)
    if request.method == 'POST':
        form = CategoriaComercialForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('comercializacion:categoria_list')
    else:
        form = CategoriaComercialForm(instance=categoria)
    return render(request, 'comercializacion/categoria_form.html', {'form': form, 'title': 'Editar Categoría'})

@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(CategoriaComercial, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('comercializacion:categoria_list')
    return render(request, 'comercializacion/categoria_confirm_delete.html', {'categoria': categoria})

# Información Comercial
@login_required
def producto_comercial_list(request):
    q = request.GET.get('q', '')
    cat_id = request.GET.get('categoria', '')
    productos = InformacionComercial.objects.select_related('producto', 'categoria').all()
    
    if q:
        productos = productos.filter(Q(nombre_comercial__icontains=q) | Q(producto__nombre__icontains=q))
    if cat_id:
        productos = productos.filter(categoria_id=cat_id)
        
    categorias = CategoriaComercial.objects.all()
    
    context = {
        'items_catalogo': productos,
        'categorias': categorias,
        'q': q,
        'cat_sel': cat_id,
    }
    return render(request, 'comercializacion/catalogo_list.html', context)

@login_required
def producto_comercial_create(request):
    if request.method == 'POST':
        form = InformacionComercialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información comercial creada exitosamente.')
            return redirect('comercializacion:catalogo_list')
    else:
        form = InformacionComercialForm()
    return render(request, 'comercializacion/catalogo_form.html', {'form': form, 'title': 'Crear Información Comercial'})

@login_required
def producto_comercial_update(request, pk):
    info = get_object_or_404(InformacionComercial, pk=pk)
    if request.method == 'POST':
        form = InformacionComercialForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información comercial actualizada exitosamente.')
            return redirect('comercializacion:catalogo_list')
    else:
        form = InformacionComercialForm(instance=info)
    return render(request, 'comercializacion/catalogo_form.html', {'form': form, 'title': 'Editar Información Comercial'})

@login_required
def producto_comercial_delete(request, pk):
    info = get_object_or_404(InformacionComercial, pk=pk)
    if request.method == 'POST':
        info.delete()
        messages.success(request, 'Información comercial eliminada exitosamente.')
        return redirect('comercializacion:catalogo_list')
    return render(request, 'comercializacion/producto_comercial_confirm_delete.html', {'info': info})

# Listas de Precio
@login_required
def lista_precio_list(request):
    listas = ListaPrecio.objects.all()
    return render(request, 'comercializacion/listas_precio_list.html', {'listas': listas})

@login_required
def lista_precio_create(request):
    if request.method == 'POST':
        form = ListaPrecioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lista de precios creada exitosamente.')
            return redirect('comercializacion:lista_precio_list')
    else:
        form = ListaPrecioForm()
    return render(request, 'comercializacion/lista_precio_form.html', {'form': form, 'title': 'Crear Lista de Precios'})

@login_required
def lista_precio_update(request, pk):
    lista = get_object_or_404(ListaPrecio, pk=pk)
    if request.method == 'POST':
        form = ListaPrecioForm(request.POST, instance=lista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lista de precios actualizada exitosamente.')
            return redirect('comercializacion:lista_precio_list')
    else:
        form = ListaPrecioForm(instance=lista)
    return render(request, 'comercializacion/lista_precio_form.html', {'form': form, 'title': 'Editar Lista de Precios'})

@login_required
def lista_precio_delete(request, pk):
    lista = get_object_or_404(ListaPrecio, pk=pk)
    if request.method == 'POST':
        lista.delete()
        messages.success(request, 'Lista de precios eliminada exitosamente.')
        return redirect('comercializacion:lista_precio_list')
    return render(request, 'comercializacion/lista_precio_confirm_delete.html', {'lista': lista})

# Items de Precio
@login_required
def item_precio_list(request, lista_id):
    lista = get_object_or_404(ListaPrecio, pk=lista_id)
    items = ItemPrecio.objects.filter(lista=lista).select_related('producto')
    return render(request, 'comercializacion/lista_precio_detail.html', {
        'lista': lista, 
        'items': items,
        'form_item': ItemPrecioForm()
    })

@login_required
def item_precio_create(request, lista_id):
    lista = get_object_or_404(ListaPrecio, pk=lista_id)
    if request.method == 'POST':
        form = ItemPrecioForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.lista = lista
            item.save()
            messages.success(request, 'Precio agregado exitosamente.')
            return redirect('comercializacion:item_precio_list', lista_id=lista_id)
    else:
        form = ItemPrecioForm()
    return render(request, 'comercializacion/item_precio_form.html', {'form': form, 'lista': lista, 'title': 'Agregar Precio'})

@login_required
def item_precio_update(request, pk):
    item = get_object_or_404(ItemPrecio, pk=pk)
    if request.method == 'POST':
        form = ItemPrecioForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Precio actualizado exitosamente.')
            return redirect('comercializacion:item_precio_list', lista_id=item.lista_id)
    else:
        form = ItemPrecioForm(instance=item)
    return render(request, 'comercializacion/item_precio_form.html', {'form': form, 'lista': item.lista, 'title': 'Editar Precio'})

@login_required
def item_precio_delete(request, pk):
    item = get_object_or_404(ItemPrecio, pk=pk)
    lista_id = item.lista_id
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Precio eliminado exitosamente.')
        return redirect('comercializacion:item_precio_list', lista_id=lista_id)
    return render(request, 'comercializacion/item_precio_confirm_delete.html', {'item': item})

@login_required
def lista_imprimir(request, pk):
    lista = get_object_or_404(ListaPrecio, pk=pk)
    items = ItemPrecio.objects.filter(lista=lista).select_related('producto')
    return render(request, 'comercializacion/lista_precio_print.html', {'lista': lista, 'items': items})

@login_required
def promocion_create(request):
    from .forms import PromocionForm
    if request.method == 'POST':
        form = PromocionForm(request.POST)
        if form.is_valid():
            productos = form.cleaned_data['productos']
            # Lógica para aplicar la promoción (ej. marcar como oferta)
            productos.update(en_oferta=True)
            messages.success(request, 'Promoción aplicada a los productos seleccionados.')
            return redirect('comercializacion:dashboard')
    else:
        form = PromocionForm()
    return render(request, 'comercializacion/promocion_form.html', {'form': form, 'titulo': 'Crear Promoción'})