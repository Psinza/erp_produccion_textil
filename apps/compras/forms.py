from django import forms
from .models import (
    OrdenCompra, FacturaCompra, DetalleFacturaCompra, ProductoCompra,
    RequerimientoMaterial, DetalleRequerimientoMaterial,
    DetalleOrdenCompra, RecepcionCompra, DetalleRecepcionCompra,
)
from apps.facturacion.models import Proveedor
from apps.produccion.models import MateriaPrima

CTR = {"class": "form-control"}
SEL = {"class": "form-select"}
NUM = {"class": "form-control", "step": "0.01"}
DATE = {"class": "form-control", "type": "date"}
TXT = {"class": "form-control", "rows": 3}

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social', 'rif', 'direccion', 'telefono', 'email']
        widgets = {
            'razon_social': forms.TextInput(attrs=CTR),
            'rif': forms.TextInput(attrs=CTR),
            'direccion': forms.Textarea(attrs=TXT),
            'telefono': forms.TextInput(attrs=CTR),
            'email': forms.EmailInput(attrs=CTR),
        }

class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['nombre', 'sku', 'categoria', 'unidad_medida', 'tipo_insumo', 'especificacion_tecnica', 'stock_minimo', 'costo_unitario', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs=CTR),
            'sku': forms.TextInput(attrs=CTR),
            'categoria': forms.Select(attrs=SEL),
            'unidad_medida': forms.Select(attrs=SEL),
            'tipo_insumo': forms.Select(attrs=SEL),
            'especificacion_tecnica': forms.TextInput(attrs=CTR),
            'stock_minimo': forms.NumberInput(attrs=NUM),
            'costo_unitario': forms.NumberInput(attrs=NUM),
            'activo': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class ProductoCompraForm(forms.ModelForm):
    class Meta:
        model = ProductoCompra
        fields = ['nombre', 'codigo', 'descripcion', 'tipo', 'unidad_medida', 'especificacion_textil', 'precio_referencia', 'moneda']
        widgets = {
            'nombre': forms.TextInput(attrs=CTR),
            'codigo': forms.TextInput(attrs=CTR),
            'descripcion': forms.Textarea(attrs=TXT),
            'tipo': forms.Select(attrs=SEL),
            'unidad_medida': forms.TextInput(attrs=CTR),
            'especificacion_textil': forms.Textarea(attrs=TXT),
            'precio_referencia': forms.NumberInput(attrs=NUM),
            'moneda': forms.Select(attrs=SEL),
        }

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'fecha_emision', 'moneda', 'estado']
        widgets = {
            'proveedor': forms.Select(attrs=SEL),
            'fecha_emision': forms.DateInput(attrs=DATE),
            'moneda': forms.Select(attrs=SEL),
            'estado': forms.Select(attrs=SEL),
        }


class RequerimientoMaterialForm(forms.ModelForm):
    class Meta:
        model = RequerimientoMaterial
        fields = ['numero', 'orden_produccion', 'solicitud_pieza', 'almacen_destino', 'estado', 'fecha_requerida', 'observaciones']
        widgets = {
            'fecha_requerida': forms.DateInput(attrs=DATE),
            'observaciones': forms.Textarea(attrs=TXT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ej: RM-2026-00001'})
        for name in ('orden_produccion', 'solicitud_pieza', 'almacen_destino', 'estado'):
            self.fields[name].widget.attrs.update(SEL)
        self.fields['orden_produccion'].empty_label = 'Seleccione una orden de producción...'
        self.fields['solicitud_pieza'].empty_label = 'Seleccione una solicitud de pieza...'
        self.fields['almacen_destino'].empty_label = 'Seleccione el almacén destino...'
        self.fields['estado'].widget.attrs.update(SEL)
        self.fields['orden_produccion'].required = False
        self.fields['solicitud_pieza'].required = False
        self.fields['almacen_destino'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('orden_produccion') and not cleaned_data.get('solicitud_pieza'):
            raise forms.ValidationError('Indique la orden de producción o la solicitud de pieza que origina el requerimiento.')
        if cleaned_data.get('orden_produccion') and cleaned_data.get('solicitud_pieza'):
            raise forms.ValidationError('Un requerimiento no puede mezclar una orden de producción y una solicitud de pieza.')
        return cleaned_data


class DetalleRequerimientoMaterialForm(forms.ModelForm):
    class Meta:
        model = DetalleRequerimientoMaterial
        fields = [
            'materia_prima', 'repuesto', 'descripcion', 'cantidad',
            'unidad_medida', 'especificacion',
        ]
        widgets = {
            'materia_prima': forms.Select(attrs=SEL),
            'repuesto': forms.Select(attrs=SEL),
            'descripcion': forms.TextInput(attrs=CTR),
            'cantidad': forms.NumberInput(attrs=NUM),
            'unidad_medida': forms.TextInput(attrs=CTR),
            'especificacion': forms.Textarea(attrs=TXT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materia_prima'].empty_label = 'Seleccione materia prima...'
        self.fields['repuesto'].empty_label = 'Seleccione repuesto...'


class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['materia_prima', 'repuesto', 'descripcion', 'cantidad', 'unidad_medida', 'precio_unitario', 'moneda']


class RecepcionCompraForm(forms.ModelForm):
    class Meta:
        model = RecepcionCompra
        fields = ['orden', 'almacen', 'factura', 'numero_acta', 'fecha', 'estado', 'observaciones']
        widgets = {'fecha': forms.DateInput(attrs=DATE), 'observaciones': forms.Textarea(attrs=TXT)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['almacen'].queryset = self.fields['almacen'].queryset.filter(
            activo=True
        )
        self.fields['almacen'].help_text = (
            'Para repuestos de máquinas seleccione el almacén de repuestos; '
            'el requerimiento puede indicar el destino recomendado.'
        )


class DetalleRecepcionCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleRecepcionCompra
        fields = ['detalle_orden', 'cantidad', 'descripcion', 'aceptado']