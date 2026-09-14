from django import forms
from apps.logistica.models import RepuestoMaquina
from .models import (
    ChequeoLineaProduccion, LineaProduccion, MaquinaTextil,
    OrdenMantenimientoTextil, PlanMantenimientoTextil, SolicitudPiezaMecanica,
    MinutaMantenimiento, TrasladoMaquina, DiagnosticoElementoMaquina,
    ActividadPlanMantenimiento,
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
        fields = [
            'maquina', 'tipo', 'descripcion', 'fecha_programada', 'estado',
            'tecnico', 'costo_estimado', 'actividades_realizadas',
            'bloqueo_seguridad_verificado', 'prueba_costura_realizada',
            'muestra_costura_aceptada', 'garantia_trabajo',
            'minuta_registrada', 'observaciones',
        ]
        widgets = {'fecha_programada': forms.DateInput(attrs={'type': 'date'}), 'fecha_cierre': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('estado') == 'completada':
            requisitos = {
                'bloqueo_seguridad_verificado': 'Debe verificarse el bloqueo y las condiciones de seguridad.',
                'prueba_costura_realizada': 'Debe registrarse la prueba de costura.',
                'muestra_costura_aceptada': 'La muestra de costura debe ser aceptada por operación.',
                'minuta_registrada': 'Debe registrarse la minuta de la intervención.',
            }
            for field, message in requisitos.items():
                if not cleaned_data.get(field):
                    self.add_error(field, message)
        return cleaned_data


class ChequeoLineaForm(forms.ModelForm):
    class Meta:
        model = ChequeoLineaProduccion
        fields = ['linea', 'fecha', 'maquinas_operativas', 'maquinas_con_falla', 'observaciones', 'liberada']
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'})}


class PlanMantenimientoForm(forms.ModelForm):
    class Meta:
        model = PlanMantenimientoTextil
        fields = [
            'nombre', 'linea', 'fecha_inicio', 'fecha_fin', 'frecuencia_dias',
            'periodicidad', 'estado', 'objetivo', 'alcance',
            'actividades_programadas', 'responsable', 'activo', 'observaciones',
        ]
        widgets = {'fecha_inicio': forms.DateInput(attrs={'type': 'date'}), 'fecha_fin': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('fecha_inicio') and cleaned_data.get('fecha_fin'):
            if cleaned_data['fecha_fin'] < cleaned_data['fecha_inicio']:
                self.add_error('fecha_fin', 'La fecha final no puede ser anterior a la fecha inicial.')
        if cleaned_data.get('estado') in {'pendiente_aprobacion', 'aprobado'} and not cleaned_data.get('actividades_programadas'):
            self.add_error('actividades_programadas', 'Defina las actividades antes de solicitar aprobación.')
        return cleaned_data


class MinutaMantenimientoForm(forms.ModelForm):
    class Meta:
        model = MinutaMantenimiento
        exclude = ['responsable']
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'}), 'actividades_realizadas': forms.Textarea(attrs={'rows': 4})}


class TrasladoMaquinaForm(forms.ModelForm):
    class Meta:
        model = TrasladoMaquina
        exclude = ['solicitado_por', 'supervisor', 'aprobado_por', 'fecha_solicitud', 'fecha_ejecucion']
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 3})}


class DiagnosticoElementoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoElementoMaquina
        exclude = ['diagnosticado_por']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'resultado': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }


class ActividadPlanMantenimientoForm(forms.ModelForm):
    class Meta:
        model = ActividadPlanMantenimiento
        exclude = ['plan']
        widgets = {'checklist': forms.Textarea(attrs={'rows': 3})}
