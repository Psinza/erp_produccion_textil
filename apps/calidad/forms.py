from django import forms
from .models import AuditoriaCalidad


class AuditoriaCalidadForm(forms.ModelForm):
    class Meta:
        model = AuditoriaCalidad
        exclude = ['inspector', 'supervisor', 'validado_por', 'fecha_validacion', 'creado_en']
        widgets = {
            'fecha_inspeccion': forms.DateInput(attrs={'type': 'date'}),
            'controles_realizados': forms.Textarea(attrs={'rows': 4}),
            'medidas_registradas': forms.Textarea(attrs={'rows': 3}),
            'defectos_observaciones': forms.Textarea(attrs={'rows': 3}),
            'decision_observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('estado') in ('aprobado', 'aprobado_observacion', 'cerrado'):
            if not cleaned_data.get('controles_realizados'):
                self.add_error('controles_realizados', 'Registre los controles ejecutados antes de validar.')
        return cleaned_data
