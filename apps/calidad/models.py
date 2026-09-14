from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AuditoriaCalidad(models.Model):
    PROCEDIMIENTOS = [
        ('corte', '01 - Verificación en proceso y despacho de corte'),
        ('arranque', '02 - Aprobación de prenda de arranque'),
        ('costura', '03 - Verificación en proceso de línea de costura'),
        ('prenda_terminada', '04 - Inspección final de prenda terminada'),
        ('bordado', '05 - Inspección de bordado y auditoría de remate'),
        ('empaque', '06 - Verificación final de prendas empacadas'),
        ('materia_prima', '07 - Verificación de avíos y telas'),
    ]
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En revisión'),
        ('aprobado', 'Aprobado'),
        ('aprobado_observacion', 'Aprobado con observación'),
        ('rechazado', 'Rechazado'),
        ('reproceso', 'En reproceso'),
        ('cerrado', 'Cerrado'),
    ]
    orden = models.ForeignKey(
        'produccion.OrdenProduccion', on_delete=models.PROTECT, null=True, blank=True,
        related_name='auditorias_calidad',
    )
    numero_orden_trabajo = models.CharField(max_length=50, blank=True)
    cliente = models.CharField(max_length=200, blank=True)
    procedimiento = models.CharField(max_length=25, choices=PROCEDIMIENTOS)
    estado = models.CharField(max_length=25, choices=ESTADOS, default='borrador')
    fecha_inspeccion = models.DateField()
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='auditorias_calidad_realizadas',
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='auditorias_calidad_supervisadas',
    )
    galpon = models.CharField(max_length=80, blank=True)
    linea_costura = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=100, blank=True)
    genero = models.CharField(max_length=80, blank=True)
    talla = models.CharField(max_length=50, blank=True)
    descripcion_prenda = models.CharField(max_length=255, blank=True)
    ficha_tecnica_referencia = models.CharField(max_length=255, blank=True)
    muestra_referencia = models.CharField(max_length=255, blank=True)
    ficha_arte_referencia = models.CharField(max_length=255, blank=True)
    cantidad_lote = models.PositiveIntegerField(default=0)
    cantidad_muestra = models.PositiveIntegerField(default=0)
    piezas_aprobadas = models.PositiveIntegerField(default=0)
    piezas_rechazadas = models.PositiveIntegerField(default=0)
    defectos_criticos = models.PositiveIntegerField(default=0)
    defectos_mayores = models.PositiveIntegerField(default=0)
    defectos_menores = models.PositiveIntegerField(default=0)
    operaciones_revisadas = models.PositiveIntegerField(default=0)
    piezas_por_operacion = models.PositiveIntegerField(default=0)
    rollos_revisados = models.PositiveIntegerField(default=0)
    conos_revisados = models.PositiveIntegerField(default=0)
    medidas_registradas = models.TextField(blank=True)
    controles_realizados = models.TextField()
    defectos_observaciones = models.TextField(blank=True)
    prueba_solidez_realizada = models.BooleanField(default=False)
    tiempo_reposo_verificado = models.BooleanField(default=False)
    ancho_util_verificado = models.BooleanField(default=False)
    simetria_verificada = models.BooleanField(default=False)
    remate_verificado = models.BooleanField(default=False)
    empaque_verificado = models.BooleanField(default=False)
    decision_observaciones = models.TextField(blank=True)
    requiere_reproceso = models.BooleanField(default=False)
    notificado_a = models.CharField(max_length=255, blank=True)
    validado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='auditorias_calidad_validadas',
    )
    fecha_validacion = models.DateField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-fecha_inspeccion', '-creado_en')

    def clean(self):
        if self.piezas_aprobadas + self.piezas_rechazadas > self.cantidad_muestra:
            raise ValidationError('Las piezas aprobadas y rechazadas no pueden superar la muestra inspeccionada.')
        if self.estado == 'aprobado' and self.piezas_rechazadas:
            raise ValidationError('Un registro con piezas rechazadas debe quedar observado, en reproceso o rechazado.')
        if self.procedimiento == 'costura' and self.piezas_por_operacion and self.piezas_por_operacion < 5:
            raise ValidationError('La auditoría de costura debe revisar al menos cinco piezas por operación.')
        if self.procedimiento == 'materia_prima' and not self.prueba_solidez_realizada:
            raise ValidationError('La inspección de materia prima debe registrar la prueba de solidez y color.')

    @property
    def porcentaje_rechazo(self):
        if not self.cantidad_muestra:
            return 0
        return round(self.piezas_rechazadas * 100 / self.cantidad_muestra, 2)

    def __str__(self):
        referencia = self.orden.lote_numero if self.orden_id else self.numero_orden_trabajo or 'sin orden'
        return f'{self.get_procedimiento_display()} - {referencia}'
