from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PlanificacionEntrega(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En revisión'),
        ('validada', 'Validada por Gerencia'),
        ('publicada', 'Publicada'),
        ('cerrada', 'Cerrada'),
    ]
    orden = models.ForeignKey(
        'produccion.OrdenProduccion', on_delete=models.PROTECT,
        related_name='planificaciones_pcpi',
    )
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_entrega_comprometida = models.DateField(null=True, blank=True)
    tiempo_estandar_minutos = models.PositiveIntegerField(default=0)
    dias_habiles_requeridos = models.PositiveIntegerField(default=0)
    secuencia_fabricacion = models.TextField()
    disponibilidad_lineas = models.TextField(blank=True)
    disponibilidad_maquinaria = models.TextField(blank=True)
    restricciones = models.TextField(blank=True)
    escenarios = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='planificaciones_pcpi',
    )
    validada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='planificaciones_pcpi_validadas',
    )
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if (
            self.fecha_entrega_comprometida
            and self.fecha_entrega_comprometida < (self.fecha_solicitud or timezone.localdate())
        ):
            raise ValidationError(
                'La fecha comprometida no puede ser anterior a la solicitud.'
            )


class ProgramacionSemanal(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En revisión'),
        ('validada', 'Validada por Gerencia'),
        ('distribuida', 'Distribuida'),
        ('cerrada', 'Cerrada'),
    ]
    semana_inicio = models.DateField()
    semana_fin = models.DateField()
    planificacion = models.ForeignKey(
        PlanificacionEntrega, on_delete=models.PROTECT,
        related_name='programaciones_semanales',
    )
    notas_entrega_materiales = models.TextField(blank=True)
    informe_calidad_materia_prima = models.TextField(blank=True)
    tiempos_estandar = models.TextField(blank=True)
    disponibilidad_maquinaria = models.TextField(blank=True)
    cuotas_produccion = models.PositiveIntegerField(default=0)
    eficiencia_referencia = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    restricciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    elaborado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='programaciones_semanales_pcpi')
    validado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='programaciones_semanales_validadas')
    distribuido_a = models.CharField(max_length=255, blank=True, help_text='UDP, Producción, Ingeniería y Calidad')
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.semana_fin < self.semana_inicio:
            raise ValidationError('La fecha final de la semana no puede ser anterior a la inicial.')
        if self.eficiencia_referencia > 100:
            raise ValidationError('La eficiencia de referencia no puede superar 100%.')


class ResumenRequerimientosMateriales(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En revisión'),
        ('emitido', 'Emitido'),
        ('validado', 'Validado y sellado'),
        ('atendido', 'Atendido por Almacén'),
        ('archivado', 'Archivado'),
    ]
    numero = models.CharField(max_length=30, unique=True)
    orden = models.ForeignKey(
        'produccion.OrdenProduccion', on_delete=models.PROTECT,
        related_name='resumenes_materiales_pcpi',
    )
    requerimiento = models.ForeignKey(
        'compras.RequerimientoMaterial', on_delete=models.PROTECT,
        null=True, blank=True, related_name='resumenes_pcpi',
    )
    hoja_consumo_referencia = models.CharField(max_length=255)
    nota_entrega_referencia = models.CharField(max_length=255, blank=True)
    materiales_transcritos = models.TextField()
    cantidad_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    unidad_medida = models.CharField(max_length=20, default='unidad')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    elaborado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='resumenes_materiales_pcpi')
    validado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resumenes_materiales_pcpi_validados')
    fecha_validacion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.estado in ('emitido', 'validado', 'atendido', 'archivado') and not self.hoja_consumo_referencia:
            raise ValidationError('El resumen emitido requiere referencia de hoja de consumo.')


class DistribucionOrdenTrabajo(models.Model):
    orden_trabajo = models.ForeignKey(
        'produccion.OrdenTrabajoProduccion', on_delete=models.CASCADE,
        related_name='distribuciones_pcpi',
    )
    unidad = models.CharField(max_length=120)
    fecha_entrega = models.DateField(null=True, blank=True)
    recibido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    recibido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
