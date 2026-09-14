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
    RegistroProduccionTurno,
    MuestraPrenda, DigitalizacionMolde, ProgramacionProduccion, OrdenTrabajoProduccion,
    MateriaPrima,
    ProductoTerminado,
    ProcesoDepartamento, IndicadorProceso, MedicionIndicador, NoConformidad
)


class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = [
            'nombre', 'tipo_prenda', 'categoria', 'sku', 'gramaje',
            'ancho', 'costo_estimado', 'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_prenda': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'gramaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'costo_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

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
            , 'requerimiento_materiales', 'ficha_tecnica', 'aprobado',
            'muestra_aprobada', 'referencia_muestra', 'observaciones_muestra',
            'referencia_archivo_audaces', 'version_molde_digital',
            'tallas_escaladas', 'hoja_medidas_molde', 'tizado_disponible'
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
            'orden', 'estado', 'orden_corte', 'fecha_programada', 'jefe_corte',
            'supervisor_mesa', 'equipo_corte', 'ruta_corte', 'mesa_corte',
            'mesa_calidad', 'mesa_habilitado', 'carro_carga',
            'instrucciones_jefatura', 'materiales_verificados',
            'observaciones_materiales', 'instrumento_tecnico', 'tizado',
            'aprovechamiento_tela', 'tela_tendida_metros', 'disenos_recibidos',
            'piezas_por_lote', 'piezas_defectuosas_corte', 'tipo_tela_validado',
            'observaciones_calidad_tela', 'control_calidad_en_proceso',
            'observaciones_calidad_proceso', 'piezas_fusionadas',
            'fusion_verificada', 'piezas_habilitadas', 'conteo_verificado',
            'paquete_completo', 'calidad_post_corte_aprobada',
            'observaciones_calidad_post', 'linea_destino', 'enviado_carro_carga',
            'corte_habilitado',
        ]
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'fecha_programada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tela_tendida_metros': forms.NumberInput(attrs={'class': 'form-control'}),
            'disenos_recibidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_por_lote': forms.NumberInput(attrs={'class': 'form-control'}),
            'piezas_defectuosas_corte': forms.NumberInput(attrs={'class': 'form-control'}),
            'instrucciones_jefatura': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipo_corte': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_materiales': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instrumento_tecnico': forms.TextInput(attrs={'class': 'form-control'}),
            'aprovechamiento_tela': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_calidad_tela': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_calidad_proceso': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_calidad_post': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('corte_habilitado') and not cleaned_data.get('tipo_tela_validado'):
            raise ValidationError('Debe validarse el tipo de tela antes de habilitar el corte.')
        if cleaned_data.get('corte_habilitado'):
            requisitos = {
                'materiales_verificados': 'Debe verificarse la existencia de materiales y consumibles.',
                'control_calidad_en_proceso': 'Debe registrarse el control de calidad durante el corte.',
                'fusion_verificada': 'Debe verificarse el fusionado antes del habilitado.',
                'conteo_verificado': 'Debe verificarse el conteo de piezas y partes.',
                'paquete_completo': 'Debe confirmarse que el paquete de corte está completo.',
                'calidad_post_corte_aprobada': 'La mesa de calidad post corte debe aprobar el paquete.',
                'enviado_carro_carga': 'Debe registrarse el envío al carro de carga.',
            }
            for field, message in requisitos.items():
                if not cleaned_data.get(field):
                    self.add_error(field, message)
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


class RegistroProduccionTurnoForm(forms.ModelForm):
    class Meta:
        model = RegistroProduccionTurno
        fields = ['orden', 'linea', 'fecha', 'turno', 'periodo', 'meta_piezas', 'piezas_buenas',
                  'piezas_rechazadas', 'minutos_planificados', 'minutos_parada', 'causa_parada',
                  'cuello_botella', 'materiales_disponibles', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data.get('minutos_parada') or 0) > (cleaned_data.get('minutos_planificados') or 0):
            self.add_error('minutos_parada', 'La parada no puede superar los minutos planificados.')
        return cleaned_data


class MuestraPrendaForm(forms.ModelForm):
    class Meta:
        model = MuestraPrenda
        exclude = ['orden', 'solicitada_por', 'aprobada_por', 'fecha_aprobacion', 'creada_en']
        widgets = {
            'requisitos_cliente': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'materiales_utilizados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'medidas_verificadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'resultado_calidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DigitalizacionMoldeForm(forms.ModelForm):
    class Meta:
        model = DigitalizacionMolde
        exclude = ['orden', 'patronista', 'analista', 'validado_por', 'creado_en']
        widgets = {
            'hoja_medidas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ProgramacionProduccionForm(forms.ModelForm):
    class Meta:
        model = ProgramacionProduccion
        exclude = ['orden', 'responsable', 'validada_por', 'creado_en']
        widgets = {
            'inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'disponibilidad_maquinaria': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'calidad_materia_prima': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'restricciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'escenario': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio, fin = cleaned_data.get('inicio'), cleaned_data.get('fin')
        if inicio and fin and fin < inicio:
            self.add_error('fin', 'La fecha final no puede ser anterior a la fecha inicial.')
        return cleaned_data


class OrdenTrabajoProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajoProduccion
        exclude = ['orden', 'numero', 'elaborada_por', 'aprobada_por', 'fecha_aprobacion', 'creado_en']
        widgets = {
            'secuencia_fabricacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cuotas_produccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
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
            'orden', 'tipo', 'origen', 'requisito', 'ubicacion', 'descripcion',
            'cantidad_afectada', 'porcentaje_rechazo', 'riesgo', 'detectada_por',
            'accion_inmediata', 'causa_raiz', 'accion_correctiva', 'tratamiento',
            'concesion', 'autoridad_concesion', 'fecha_verificacion',
            'criterio_eficacia', 'resultado_eficacia', 'eficaz', 'estado',
            'responsable',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'requisito': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'accion_inmediata': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'causa_raiz': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'accion_correctiva': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'concesion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'criterio_eficacia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'resultado_eficacia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha_verificacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        tratamiento = cleaned_data.get('tratamiento')
        if tipo == 'snc' and tratamiento == 'liberacion' and not cleaned_data.get('concesion'):
            self.add_error('concesion', 'Una liberación bajo concesión requiere autorización documentada.')
        if cleaned_data.get('estado') == 'cerrada' and not cleaned_data.get('eficaz'):
            self.add_error('eficaz', 'La NC/OM/SNC solo puede cerrarse después de verificar su eficacia.')
        return cleaned_data