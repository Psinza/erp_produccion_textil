from django import forms
from django.core.exceptions import ValidationError
from .models import (
    OrdenProduccion,
    DepartamentoUDP,
    DepartamentoCorte,
    DepartamentoProduccionTextil,
    DepartamentoBordado,
    DepartamentoDespacho,
    DepartamentoCalidadISO9001,
    MateriaPrima,
    ProductoTerminado,
    ProcesoDepartamento, IndicadorProceso, MedicionIndicador, NoConformidad
)

class OrdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = ['lote_numero', 'producto', 'cantidad_a_producir', 'estado', 'prioridad', 'fecha_planificada', 'responsable', 'observaciones']
        widgets = {
            'lote_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_a_producir': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'fecha_planificada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DepartamentoUDPForm(forms.ModelForm):
    class Meta:
        model = DepartamentoUDP
        fields = [
            'orden', 'proyecto', 'tipo_uniforme', 'tipo_diseno', 
            'cantidad_disenos', 'piezas_por_diseno', 'rango_tallas', 
            'tipo_tela', 'especificaciones_tecnicas'
            , 'requerimiento_materiales', 'ficha_tecnica', 'aprobado'
        ]
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del lote o proyecto'}),
            'tipo_uniforme': forms.Select(attrs={'class': 'form-select'}),
            'tipo_diseno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Camisolas y pantalones tácticos'}),
            'cantidad_disenos': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_por_diseno': forms.NumberInput(attrs={'class': 'form-control'}),
            'rango_tallas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. XS a 3XL / Tallas 28 a 44'}),
            'tipo_tela': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ripstop 65% poliéster 35% algodón'}),
            'especificaciones_tecnicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Gramaje superior a 280 g/m², acabados repelentes, etc.'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('aprobado') and not cleaned_data.get('ficha_tecnica'):
            raise ValidationError('La ficha técnica es obligatoria para aprobar UDP.')
        if cleaned_data.get('aprobado') and not cleaned_data.get('requerimiento_materiales'):
            raise ValidationError('El requerimiento de materiales es obligatorio para aprobar UDP.')
        return cleaned_data

class DepartamentoCorteForm(forms.ModelForm):
    class Meta:
        model = DepartamentoCorte
        fields = [
            'orden', 'tela_tendida_metros', 'disenos_recibidos', 'piezas_por_lote',
            'piezas_defectuosas_corte', 'tipo_tela_validado',
            'observaciones_calidad_tela', 'corte_habilitado',
        ]
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'tela_tendida_metros': forms.NumberInput(attrs={'class': 'form-control'}),
            'disenos_recibidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_por_lote': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_defectuosas_corte': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('corte_habilitado') and not cleaned_data.get('tipo_tela_validado'):
            raise ValidationError('Debe validarse el tipo de tela antes de habilitar el corte.')
        return cleaned_data

class DepartamentoProduccionForm(forms.ModelForm):
    class Meta:
        model = DepartamentoProduccionTextil
        fields = ['orden', 'linea_produccion', 'productos_realizados', 'piezas_con_falla_costura']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'linea_produccion': forms.TextInput(attrs={'class': 'form-control'}),
            'productos_realizados': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_con_falla_costura': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DepartamentoBordadoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoBordado
        fields = ['orden', 'operario', 'descripcion_bordado', 'piezas_bordadas_ok', 'piezas_rechazadas_bordado']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'operario': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_bordado': forms.TextInput(attrs={'class': 'form-control'}),
            'piezas_bordadas_ok': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_rechazadas_bordado': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DepartamentoDespachoForm(forms.ModelForm):
    class Meta:
        model = DepartamentoDespacho
        fields = [
            'orden', 'responsable_empaque', 'planchado_ok', 'empaquetado_ok',
            'piezas_empaquetadas', 'fibras_hilos_sueltos_ok', 'observaciones_revision',
        ]
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'responsable_empaque': forms.Select(attrs={'class': 'form-select'}),
            'planchado_ok': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'empaquetado_ok': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'piezas_empaquetadas': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('empaquetado_ok') and not cleaned_data.get('planchado_ok'):
            raise ValidationError('El planchado debe estar conforme antes de empaquetar.')
        if cleaned_data.get('empaquetado_ok') and not cleaned_data.get('fibras_hilos_sueltos_ok'):
            raise ValidationError('Debe aprobarse la revisión de fibras e hilos sueltos.')
        return cleaned_data

class DepartamentoCalidadISOForm(forms.ModelForm):
    class Meta:
        model = DepartamentoCalidadISO9001
        fields = ['orden', 'auditor', 'cumple_iso_9001', 'gramaje_verificado', 'piezas_aprobadas_qc', 'piezas_rechazadas_qc', 'informe_auditoria']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'auditor': forms.Select(attrs={'class': 'form-select'}),
            'cumple_iso_9001': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gramaje_verificado': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_aprobadas_qc': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_rechazadas_qc': forms.NumberInput(attrs={'class': 'form-control'}),
            'informe_auditoria': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ProcesoDepartamentoForm(forms.ModelForm):
    class Meta:
        model = ProcesoDepartamento
        exclude = ['version', 'fecha_aprobacion', 'creado_en', 'actualizado_en']
        widgets = {
            'entradas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'actividades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'salidas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'criterios_aceptacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MedicionIndicadorForm(forms.ModelForm):
    class Meta:
        model = MedicionIndicador
        fields = ['indicador', 'orden', 'valor', 'periodo', 'observaciones']
        widgets = {
            'periodo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class NoConformidadForm(forms.ModelForm):
    class Meta:
        model = NoConformidad
        fields = [
            'orden', 'origen', 'descripcion', 'cantidad_afectada',
            'porcentaje_rechazo', 'accion_inmediata', 'causa_raiz',
            'accion_correctiva', 'estado', 'responsable',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'accion_inmediata': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'causa_raiz': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'accion_correctiva': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }