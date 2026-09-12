from django import forms
from django.utils import timezone
from .models import Cotizacion, Pedido, Cliente, ProductoVenta, DetallePedido, CategoriaCliente

class CategoriaClienteForm(forms.ModelForm):
    class Meta:
        model = CategoriaCliente
        fields = ['nombre', 'descuento_pct', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cliente institucional'}),
            'descuento_pct': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'fecha_emision', 'moneda', 'estado', 'descuento_total', 'impuesto_total']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'descuento_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'impuesto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'cliente', 'fecha_pedido', 'moneda', 'dias_credito', 'direccion_despacho',
            'iva_porcentaje', 'descuento_global_porcentaje', 'observaciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha_pedido': forms.DateInput(attrs={'type': 'date'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'direccion_despacho': forms.Textarea(attrs={'rows': 3}),
            'dias_credito': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'iva_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'descuento_global_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'max': 100}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].empty_label = 'Seleccione un comprador...'
        self.fields['cliente'].queryset = Cliente.objects.filter(estado='activo').order_by('razon_social')

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'precio_unitario', 'orden_produccion', 'observaciones']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = ProductoVenta.objects.filter(activo=True).order_by('nombre')
        self.fields['producto'].empty_label = 'Seleccione un producto...'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriaCliente.objects.order_by('nombre')
        self.fields['categoria'].empty_label = 'Seleccione una categoría...'
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

class ProductoVentaForm(forms.ModelForm):
    class Meta:
        model = ProductoVenta
        fields = [
            'codigo', 'nombre', 'categoria', 'producto_base', 'precio_venta',
            'impuesto_pct', 'moneda', 'tipo_producto', 'composicion_textil',
            'tallas', 'colores', 'es_sobre_pedido', 'activo',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'producto_base': forms.Select(attrs={'class': 'form-select'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'impuesto_pct': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'moneda': forms.Select(
                choices=[('VES', 'Bolívares (VES)'), ('USD', 'Dólares (USD)'), ('EUR', 'Euros (EUR)')],
                attrs={'class': 'form-select'},
            ),
            'tipo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'composicion_textil': forms.TextInput(attrs={'class': 'form-control'}),
            'tallas': forms.TextInput(attrs={'class': 'form-control'}),
            'colores': forms.TextInput(attrs={'class': 'form-control'}),
            'es_sobre_pedido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }