from django import forms
from .models import (
    OrdenProduccion,
    DepartamentoUDP,
    DepartamentoCorte,
    DepartamentoProduccionTextil,
    DepartamentoBordado,
    DepartamentoDespacho,
    DepartamentoCalidadISO9001,
    MateriaPrima,
    ProductoTerminado
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

class DepartamentoCorteForm(forms.ModelForm):
    class Meta:
        model = DepartamentoCorte
        fields = ['orden', 'tela_tendida_metros', 'disenos_recibidos', 'piezas_por_lote', 'piezas_defectuosas_corte']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'tela_tendida_metros': forms.NumberInput(attrs={'class': 'form-control'}),
            'disenos_recibidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_por_lote': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_defectuosas_corte': forms.NumberInput(attrs={'class': 'form-control'}),
        }

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
        fields = ['orden', 'responsable_empaque', 'planchado_ok', 'empaquetado_ok', 'piezas_empaquetadas']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'responsable_empaque': forms.Select(attrs={'class': 'form-select'}),
            'planchado_ok': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'empaquetado_ok': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'piezas_empaquetadas': forms.NumberInput(attrs={'class': 'form-control'}),
        }

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