from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from apps.core.models import AsientoContable, LineaAsiento, CuentaContable, EjercicioContable

CTR = {"class": "form-control"}
SEL = {"class": "form-select"}
NUM = {"class": "form-control", "step": "0.01"}
DATE = {"class": "form-control", "type": "date"}

class AsientoContableForm(forms.ModelForm):
    class Meta:
        model = AsientoContable
        fields = ['fecha', 'tipo', 'descripcion', 'referencia', 'ejercicio', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs=DATE),
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Concepto del asiento...'}),
            'tipo': forms.Select(attrs=SEL),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Factura, pedido u otro documento'}),
            'ejercicio': forms.Select(attrs=SEL),
            'estado': forms.Select(attrs=SEL),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ejercicio'].empty_label = 'Seleccione un ejercicio...'
        self.fields['tipo'].empty_label = 'Seleccione un tipo...'


class ReporteContableForm(forms.Form):
    ejercicio = forms.ModelChoiceField(
        queryset=EjercicioContable.objects.order_by('-fecha_inicio'),
        required=True, empty_label='Seleccione un ejercicio...',
        label='Ejercicio fiscal',
        widget=forms.Select(attrs=SEL),
    )
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs=DATE))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs=DATE))

class LineaAsientoForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=[('debe', 'Debe'), ('haber', 'Haber')], widget=forms.Select(attrs=SEL))
    monto = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.NumberInput(attrs=NUM))

    class Meta:
        model = LineaAsiento
        fields = ['cuenta', 'descripcion']
        widgets = {
            'cuenta': forms.Select(attrs=SEL),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Referencia...'}),
        }

LineaAsientoFormSet = inlineformset_factory(
    AsientoContable, LineaAsiento,
    form=LineaAsientoForm,
    extra=5,
    can_delete=True
)

class CuentaContableForm(forms.ModelForm):
    acepta_movimientos = forms.BooleanField(
        required=False,
        initial=True,
        label='Acepta movimientos',
        help_text='Desactive esta opción para usar la cuenta solo como agrupadora.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = CuentaContable
        fields = [
            'codigo', 'nombre', 'tipo', 'naturaleza', 'nivel', 'padre',
            'saldo_inicial', 'acepta_movimientos', 'activo', 'descripcion',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={**CTR, 'placeholder': 'Ej: 1.1.01'}),
            'nombre': forms.TextInput(attrs={**CTR, 'placeholder': 'Nombre de la cuenta'}),
            'tipo': forms.Select(attrs=SEL),
            'naturaleza': forms.Select(attrs=SEL),
            'nivel': forms.NumberInput(attrs={**CTR, 'min': 1, 'max': 10}),
            'padre': forms.Select(attrs=SEL),
            'saldo_inicial': forms.NumberInput(attrs=NUM),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].empty_label = 'Seleccione un tipo...'
        self.fields['naturaleza'].empty_label = 'Seleccione una naturaleza...'
        self.fields['padre'].queryset = CuentaContable.objects.order_by('codigo')
        self.fields['padre'].empty_label = 'Sin cuenta padre (cuenta principal)'
        if self.instance.pk:
            self.fields['acepta_movimientos'].initial = not self.instance.es_cuenta_mayor

    def clean(self):
        cleaned_data = super().clean()
        padre = cleaned_data.get('padre')
        if self.instance.pk and padre and padre.pk == self.instance.pk:
            raise forms.ValidationError('Una cuenta no puede ser su propia cuenta padre.')
        if cleaned_data.get('nivel', 1) > 1 and not padre:
            raise forms.ValidationError('Las subcuentas deben tener una cuenta padre.')
        return cleaned_data

    def save(self, commit=True):
        cuenta = super().save(commit=False)
        cuenta.es_cuenta_mayor = not self.cleaned_data.get('acepta_movimientos', True)
        if commit:
            cuenta.save()
        return cuenta

class EjercicioContableForm(forms.ModelForm):
    class Meta:
        model = EjercicioContable
        fields = ['nombre', 'ano', 'fecha_inicio', 'fecha_fin', 'cerrado']
        widgets = {
            'nombre': forms.TextInput(attrs=CTR),
            'ano': forms.NumberInput(attrs={**CTR, 'min': 2000, 'max': 2100, 'placeholder': 'Ej: 2026'}),
            'fecha_inicio': forms.DateInput(attrs=DATE),
            'fecha_fin': forms.DateInput(attrs=DATE),
            'cerrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ano'].initial = timezone.localdate().year

    def clean(self):
        cleaned = super().clean()
        ano = cleaned.get('ano')
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        if inicio and fin and fin < inicio:
            raise forms.ValidationError('La fecha fin no puede ser anterior a la fecha de inicio.')
        if ano and inicio and inicio.year != ano:
            raise forms.ValidationError('El año de la fecha de inicio debe coincidir con el año del ejercicio.')
        if ano and fin and fin.year != ano:
            raise forms.ValidationError('El año de la fecha fin debe coincidir con el año del ejercicio.')
        return cleaned