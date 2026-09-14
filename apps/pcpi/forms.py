from django import forms
from .models import (
    PlanificacionEntrega, ProgramacionSemanal,
    ResumenRequerimientosMateriales, DistribucionOrdenTrabajo,
)


class PlanificacionEntregaForm(forms.ModelForm):
    class Meta:
        model = PlanificacionEntrega
        exclude = ['responsable', 'validada_por', 'creado_en']
        widgets = {
            'fecha_entrega_comprometida': forms.DateInput(attrs={'type': 'date'}),
            'secuencia_fabricacion': forms.Textarea(attrs={'rows': 3}),
            'disponibilidad_lineas': forms.Textarea(attrs={'rows': 2}),
            'disponibilidad_maquinaria': forms.Textarea(attrs={'rows': 2}),
            'restricciones': forms.Textarea(attrs={'rows': 2}),
            'escenarios': forms.Textarea(attrs={'rows': 2}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }


class ProgramacionSemanalForm(forms.ModelForm):
    class Meta:
        model = ProgramacionSemanal
        exclude = ['elaborado_por', 'validado_por', 'creado_en']
        widgets = {
            'semana_inicio': forms.DateInput(attrs={'type': 'date'}),
            'semana_fin': forms.DateInput(attrs={'type': 'date'}),
            'notas_entrega_materiales': forms.Textarea(attrs={'rows': 2}),
            'informe_calidad_materia_prima': forms.Textarea(attrs={'rows': 2}),
            'tiempos_estandar': forms.Textarea(attrs={'rows': 2}),
            'disponibilidad_maquinaria': forms.Textarea(attrs={'rows': 2}),
            'restricciones': forms.Textarea(attrs={'rows': 2}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }


class ResumenRequerimientosMaterialesForm(forms.ModelForm):
    class Meta:
        model = ResumenRequerimientosMateriales
        exclude = ['elaborado_por', 'validado_por', 'fecha_validacion', 'creado_en']
        widgets = {
            'materiales_transcritos': forms.Textarea(attrs={'rows': 4}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }


class DistribucionOrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = DistribucionOrdenTrabajo
        exclude = ['orden_trabajo', 'recibido_por', 'creado_en']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }
