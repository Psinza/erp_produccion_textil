from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.db import transaction
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from decimal import Decimal
from .models import Cliente, ProductoVenta, Pedido, Cotizacion, DetallePedido, CategoriaCliente
from .forms import ClienteForm, CotizacionForm, ProductoVentaForm, PedidoForm, DetallePedidoForm, CategoriaClienteForm

PedidoDetalleFormSet = inlineformset_factory(
    Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True
)

def render_to_pdf(template_src, context_dict={}):
    from xhtml2pdf import pisa

    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    mes_actual = hoy.month
    anho_actual = hoy.year

    pedidos_hoy = Pedido.objects.filter(fecha_pedido=hoy).count()
    
    ventas_mes = Pedido.objects.filter(
        fecha_pedido__year=anho_actual,
        fecha_pedido__month=mes_actual,
        estado__in=['confirmado', 'enviado', 'entregado']
    )
    monto_ventas_mes = sum(p.total for p in ventas_mes) or Decimal('0.00')

    context = {
        'titulo': 'Gestión de Ventas',
        'clientes_count': Cliente.objects.count(),
        'stats': {
            'monto_ventas_mes': monto_ventas_mes,
            'pedidos_hoy': pedidos_hoy,
        }
    }
    return render(request, 'ventas/dashboard.html', context)

@login_required
def cliente_list(request):
    clientes = Cliente.objects.all().order_by('razon_social')
    return render(request, 'ventas/cliente_list.html', {'clientes': clientes})

@login_required
def exportar_clientes_pdf(request):
    clientes = Cliente.objects.all().order_by('razon_social')
    data = {
        'clientes': clientes,
        'titulo': 'Reporte Maestro de Clientes'
    }
    return render_to_pdf('ventas/clientes_list_pdf.html', data)

@login_required
def disponibilidad_productos(request):
    stock_minimo = request.GET.get('stock_minimo')
    productos = ProductoVenta.objects.select_related('producto_base').all()
    if stock_minimo:
        try:
            min_val = float(stock_minimo)
            productos = productos.filter(producto_base__stock_actual__lte=min_val)
        except ValueError:
            pass
    return render(request, 'ventas/disponibilidad.html', {
        'productos': productos,
        'stock_minimo_filtro': stock_minimo,
    })

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'ventas/cliente_form.html', {'form': form, 'titulo': 'Nuevo Cliente'})


@login_required
def categoria_cliente_list(request):
    categorias = CategoriaCliente.objects.annotate(num=Count('clientes')).order_by('nombre')
    return render(request, 'ventas/categoria_cliente_list.html', {
        'categorias': categorias,
        'titulo': 'Categorías de Cliente',
    })


@login_required
def categoria_cliente_create(request):
    form = CategoriaClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ventas:categoria_cliente_list')
    return render(request, 'ventas/categoria_cliente_form.html', {
        'form': form,
        'titulo': 'Nueva categoría de cliente',
    })


@login_required
def categoria_cliente_edit(request, pk):
    categoria = get_object_or_404(CategoriaCliente, pk=pk)
    form = CategoriaClienteForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ventas:categoria_cliente_list')
    return render(request, 'ventas/categoria_cliente_form.html', {
        'form': form,
        'titulo': 'Editar categoría de cliente',
    })

@login_required
def producto_list(request):
    productos = ProductoVenta.objects.all()
    return render(request, 'ventas/producto_list.html', {'productos': productos, 'titulo': 'Lista de Productos'})

@login_required
def producto_create(request):
    form = ProductoVentaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ventas:producto_list')
    return render(request, 'ventas/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto Terminado'})

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(ProductoVenta, pk=pk)
    form = ProductoVentaForm(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ventas:producto_list')
    return render(request, 'ventas/producto_form.html', {'form': form, 'titulo': 'Editar Producto Terminado'})


@login_required
def producto_create(request):
    form = ProductoVentaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ventas:producto_list')
    return render(request, 'ventas/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto Terminado'})


@login_required
def producto_update(request, pk):
    producto = get_object_or_404(ProductoVenta, pk=pk)
    form = ProductoVentaForm(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('ventas:producto_list')
    return render(request, 'ventas/producto_form.html', {'form': form, 'titulo': 'Editar Producto Terminado'})

@login_required
def pedido_list(request):
    pedidos = Pedido.objects.select_related('cliente').prefetch_related('items__producto__producto_base').order_by('-fecha_pedido')
    return render(request, 'ventas/pedido_list.html', {
        'titulo': 'Lista de Pedidos',
        'pedidos': pedidos,
        'estados': Pedido.ESTADO_CHOICES,
    })

@login_required
def pedido_create(request):
    form = PedidoForm(request.POST or None)
    formset = PedidoDetalleFormSet(request.POST or None)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            pedido = form.save(commit=False)
            pedido.creado_por = request.user
            pedido.save()
            formset.instance = pedido
            formset.save()
            pedido.calcular_totales()
            pedido.save(update_fields=[
                'subtotal', 'base_imponible', 'descuento_total',
                'impuesto_total', 'total',
            ])
        return redirect('ventas:pedido_list')
    return render(request, 'ventas/pedido_form.html', {
        'titulo': 'Nuevo Pedido',
        'form': form,
        'formset': formset,
    })


@login_required
def generar_produccion_pedido(request, pk):
    from django.contrib import messages
    from apps.produccion.services import generar_orden_desde_detalle_pedido
    pedido = get_object_or_404(Pedido, pk=pk)
    detalles = pedido.items.select_related('producto__producto_base')
    creadas = []
    for detalle in detalles:
        try:
            creadas.append(generar_orden_desde_detalle_pedido(detalle, request.user))
        except ValueError as exc:
            messages.error(request, str(exc))
    if creadas:
        messages.success(request, f'{len(creadas)} orden(es) de producción generada(s).')
    return redirect('ventas:pedido_list')


@login_required
def generar_produccion_cotizacion(request, pk):
    from django.contrib import messages
    from apps.produccion.services import generar_orden_desde_detalle_cotizacion
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    creadas = []
    for detalle in cotizacion.items.select_related('producto__producto_base'):
        try:
            creadas.append(generar_orden_desde_detalle_cotizacion(detalle, request.user))
        except ValueError as exc:
            messages.error(request, str(exc))
    if creadas:
        messages.success(request, f'{len(creadas)} orden(es) generada(s) desde la cotización.')
    return redirect('ventas:cotizacion_list')

@login_required
def cotizacion_list(request):
    cotizaciones = Cotizacion.objects.select_related('cliente').order_by('-fecha_emision')
    return render(request, 'ventas/cotizacion_list.html', {
        'titulo': 'Lista de Cotizaciones',
        'cotizaciones': cotizaciones,
        'estados': Cotizacion.ESTADO_CHOICES if hasattr(Cotizacion, 'ESTADO_CHOICES') else [],
    })

@login_required
def cotizacion_create(request):
    form = CotizacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cotizacion = form.save(commit=False)
        cotizacion.numero = f'{timezone.now():%Y%m%d%H%M%S}'
        cotizacion.save()
        return redirect('ventas:cotizacion_list')
    return render(request, 'ventas/cotizacion_form.html', {
        'titulo': 'Nueva Cotización',
        'form': form,
    })