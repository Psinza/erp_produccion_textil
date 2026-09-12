from django import forms
from .models import MovimientoInventario, Almacen, RepuestoMaquina
from apps.produccion.models import MateriaPrima, ProductoTerminado

CTR = {"class": "form-control"}
SEL = {"class": "form-select"}
NUM = {"class": "form-control", "step": "0.01"}
DATE = {"class": "form-control", "type": "date"}
TXT = {"class": "form-control", "rows": 3}

class MovimientoInventarioForm(forms.ModelForm):
    item_tipo = forms.ChoiceField(
        choices=[('mp', 'Materia Prima'), ('pt', 'Producto Terminado'), ('repuesto', 'Repuesto de máquina')],
        widget=forms.Select(attrs=SEL),
        label="Tipo de Item"
    )
    
    class Meta:
        model = MovimientoInventario
        fields = [
            'tipo', 'motivo', 'materia_prima', 'producto_pt', 'repuesto',
            'almacen_origen', 'almacen_destino', 'cantidad', 'referencia'
        ]
        widgets = {
            'tipo': forms.Select(attrs=SEL),
            'motivo': forms.Select(attrs=SEL),
            'materia_prima': forms.Select(attrs=SEL),
            'producto_pt': forms.Select(attrs=SEL),
            'repuesto': forms.Select(attrs=SEL),
            'almacen_origen': forms.Select(attrs=SEL),
            'almacen_destino': forms.Select(attrs=SEL),
            'cantidad': forms.NumberInput(attrs=NUM),
            'referencia': forms.TextInput(attrs=CTR),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materia_prima'].required = False
        self.fields['producto_pt'].required = False
        self.fields['repuesto'].required = False
        self.fields['almacen_origen'].required = False
        self.fields['almacen_destino'].required = False

    def clean(self):
        cleaned_data = super().clean()
        items = [cleaned_data.get(name) for name in ('materia_prima', 'producto_pt', 'repuesto')]
        if sum(item is not None for item in items) != 1:
            raise forms.ValidationError('Seleccione exactamente un artículo.')
        if cleaned_data.get('tipo') == 'E' and not cleaned_data.get('almacen_destino'):
            self.add_error('almacen_destino', 'Seleccione el almacén que recibe el artículo.')
        if cleaned_data.get('tipo') == 'S' and not cleaned_data.get('almacen_origen'):
            self.add_error('almacen_origen', 'Seleccione el almacén del que sale el artículo.')
        return cleaned_data

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ['nombre', 'tipo', 'ubicacion', 'es_principal', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs=CTR),
            'tipo': forms.Select(attrs=SEL),
            'ubicacion': forms.TextInput(attrs=CTR),
            'es_principal': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'activo': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class RepuestoMaquinaForm(forms.ModelForm):
    class Meta:
        model = RepuestoMaquina
        fields = [
            'codigo', 'nombre', 'tipo', 'maquina_compatible',
            'unidad_medida', 'stock_minimo', 'costo_unitario', 'activo',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs=CTR),
            'nombre': forms.TextInput(attrs=CTR),
            'tipo': forms.Select(attrs=SEL),
            'maquina_compatible': forms.TextInput(attrs=CTR),
            'unidad_medida': forms.TextInput(attrs=CTR),
            'stock_minimo': forms.NumberInput(attrs=NUM),
            'costo_unitario': forms.NumberInput(attrs=NUM),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }