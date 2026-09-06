from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from decimal import Decimal
from xhtml2pdf import pisa
from .models import Cliente, ProductoVenta, Pedido
from .forms import ClienteForm

def render_to_pdf(template_src, context_dict={}):
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
def producto_list(request):
    productos = ProductoVenta.objects.all()
    return render(request, 'ventas/producto_list.html', {'productos': productos, 'titulo': 'Lista de Productos'})

@login_required
def pedido_list(request):
    return render(request, 'ventas/pedido_list.html', {'titulo': 'Lista de Pedidos'})

@login_required
def pedido_create(request):
    return render(request, 'ventas/pedido_form.html', {'titulo': 'Nuevo Pedido'})

@login_required
def cotizacion_list(request):
    return render(request, 'ventas/cotizacion_list.html', {'titulo': 'Lista de Cotizaciones'})

@login_required
def cotizacion_create(request):
    return render(request, 'ventas/cotizacion_form.html', {'titulo': 'Nueva Cotización'})