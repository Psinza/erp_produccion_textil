from django import forms
from apps.logistica.models import RepuestoMaquina
from .models import (
    ChequeoLineaProduccion, LineaProduccion, MaquinaTextil,
    OrdenMantenimientoTextil, PlanMantenimientoTextil, SolicitudPiezaMecanica,
)


class LineaProduccionForm(forms.ModelForm):
    class Meta:
        model = LineaProduccion
        fields = ['codigo', 'nombre', 'capacidad_diaria', 'activa']


class MaquinaTextilForm(forms.ModelForm):
    class Meta:
        model = MaquinaTextil
        fields = ['codigo', 'nombre', 'tipo', 'marca', 'modelo', 'serial', 'linea', 'ubicacion', 'estado', 'horas_operacion', 'proximo_mantenimiento', 'activa']
        widgets = {'proximo_mantenimiento': forms.DateInput(attrs={'type': 'date'})}


class SolicitudPiezaForm(forms.ModelForm):
    pieza = forms.ModelChoiceField(
        queryset=RepuestoMaquina.objects.filter(activo=True),
        required=False,
        empty_label='-- Repuesto existente (opcional) --',
        label='Pieza del stock',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = SolicitudPiezaMecanica
        fields = ['maquina', 'pieza', 'pieza_nueva', 'especificacion_pieza', 'cantidad', 'prioridad', 'motivo']
        widgets = {
            'pieza': forms.Select(attrs={'class': 'form-select'}),
            'pieza_nueva': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Motor 220V para máquina overlock',
            }),
            'especificacion_pieza': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Medidas, marca, modelo o características requeridas',
            }),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pieza = cleaned_data.get('pieza')
        pieza_nueva = (cleaned_data.get('pieza_nueva') or '').strip()
        if not pieza and not pieza_nueva:
            raise forms.ValidationError('Seleccione un repuesto existente o escriba el nombre de la pieza nueva.')
        if pieza and pieza_nueva:
            raise forms.ValidationError('Seleccione solo una opción: repuesto existente o pieza nueva.')
        return cleaned_data


class OrdenMantenimientoForm(forms.ModelForm):
    class Meta:
        model = OrdenMantenimientoTextil
        fields = ['maquina', 'tipo', 'descripcion', 'fecha_programada', 'estado', 'tecnico', 'costo_estimado', 'observaciones']
        widgets = {'fecha_programada': forms.DateInput(attrs={'type': 'date'}), 'fecha_cierre': forms.DateInput(attrs={'type': 'date'})}


class ChequeoLineaForm(forms.ModelForm):
    class Meta:
        model = ChequeoLineaProduccion
        fields = ['linea', 'fecha', 'maquinas_operativas', 'maquinas_con_falla', 'observaciones', 'liberada']
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'})}


class PlanMantenimientoForm(forms.ModelForm):
    class Meta:
        model = PlanMantenimientoTextil
        fields = ['nombre', 'linea', 'fecha_inicio', 'fecha_fin', 'frecuencia_dias', 'responsable', 'activo', 'observaciones']
        widgets = {'fecha_inicio': forms.DateInput(attrs={'type': 'date'}), 'fecha_fin': forms.DateInput(attrs={'type': 'date'})}
