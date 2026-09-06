from django import forms
from .models import Cotizacion, Pedido, Cliente, ProductoVenta, DetallePedido, CategoriaCliente

class CategoriaClienteForm(forms.ModelForm):
    class Meta:
        model = CategoriaCliente
        fields = '__all__'

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'cliente', 'fecha_pedido', 'dias_credito', 'direccion_despacho',
            'iva_porcentaje', 'descuento_global_porcentaje', 'observaciones'
        ]
        widgets = {
            'fecha_pedido': forms.DateInput(attrs={'type': 'date'}),
            'direccion_despacho': forms.Textarea(attrs={'rows': 3}),
        }

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'precio_unitario', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoVentaForm(forms.ModelForm):
    class Meta:
        model = ProductoVenta
        fields = '__all__'