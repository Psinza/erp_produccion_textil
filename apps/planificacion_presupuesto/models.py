from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class PlanEstrategico(models.Model):
    ESTADOS = [('borrador', 'Borrador'), ('aprobado', 'Aprobado'), ('vigente', 'Vigente'), ('cerrado', 'Cerrado')]
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=220)
    periodo_desde = models.PositiveIntegerField()
    periodo_hasta = models.PositiveIntegerField()
    objetivos = models.TextField()
    indicadores = models.TextField(blank=True)
    responsable = models.CharField(max_length=180)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='borrador')
    documento = models.FileField(upload_to='planificacion/planes/%Y/', blank=True)

    def clean(self):
        if self.periodo_hasta < self.periodo_desde:
            raise ValidationError({'periodo_hasta': 'Debe ser mayor o igual al año inicial.'})

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ObjetivoInstitucional(models.Model):
    plan = models.ForeignKey(PlanEstrategico, on_delete=models.CASCADE, related_name='objetivos_institucionales')
    codigo = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=250)
    linea_base = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    meta = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    unidad_medida = models.CharField(max_length=50)
    responsable = models.CharField(max_length=180)
    avance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        unique_together = ('plan', 'codigo')


class EjercicioPresupuestario(models.Model):
    ESTADOS = [('formulacion', 'En formulación'), ('aprobado', 'Aprobado'), ('ejecucion', 'En ejecución'), ('cerrado', 'Cerrado')]
    anio = models.PositiveIntegerField(unique=True)
    moneda = models.CharField(max_length=3, default='VES')
    monto_aprobado = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    fecha_aprobacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='formulacion')
    instrumento_aprobacion = models.CharField(max_length=150, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return str(self.anio)


class UnidadPresupuestaria(models.Model):
    ejercicio = models.ForeignKey(EjercicioPresupuestario, on_delete=models.CASCADE, related_name='unidades')
    codigo = models.CharField(max_length=30)
    nombre = models.CharField(max_length=180)
    responsable = models.CharField(max_length=180)
    objetivo = models.TextField(blank=True)

    class Meta:
        unique_together = ('ejercicio', 'codigo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class PartidaPresupuestaria(models.Model):
    ejercicio = models.ForeignKey(EjercicioPresupuestario, on_delete=models.CASCADE, related_name='partidas')
    codigo = models.CharField(max_length=40)
    denominacion = models.CharField(max_length=220)
    unidad = models.ForeignKey(UnidadPresupuestaria, on_delete=models.PROTECT, related_name='partidas')
    asignado = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    comprometido = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    causado = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    fuente_financiamiento = models.CharField(max_length=150, blank=True)

    class Meta:
        unique_together = ('ejercicio', 'codigo', 'unidad')

    def clean(self):
        for field in ('asignado', 'comprometido', 'causado', 'pagado'):
            if getattr(self, field) < 0:
                raise ValidationError({field: 'No puede ser negativo.'})
        if self.comprometido > self.asignado:
            raise ValidationError({'comprometido': 'No puede superar el monto asignado.'})
        if self.causado > self.comprometido:
            raise ValidationError({'causado': 'No puede superar el comprometido.'})
        if self.pagado > self.causado:
            raise ValidationError({'pagado': 'No puede superar el causado.'})


class ModificacionPresupuestaria(models.Model):
    TIPOS = [('credito_adicional', 'Crédito adicional'), ('traspaso', 'Traspaso'), ('rectificacion', 'Rectificación'), ('reduccion', 'Reducción')]
    ESTADOS = [('solicitada', 'Solicitada'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('aplicada', 'Aplicada')]
    numero = models.CharField(max_length=40, unique=True)
    ejercicio = models.ForeignKey(EjercicioPresupuestario, on_delete=models.PROTECT, related_name='modificaciones')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    justificacion = models.TextField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitada')
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    instrumento = models.CharField(max_length=150, blank=True)

    def clean(self):
        if self.monto <= 0:
            raise ValidationError({'monto': 'Debe ser mayor que cero.'})


class NormaPresupuesto(models.Model):
    jurisdiccion = models.CharField(max_length=80, default='Venezuela')
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=250)
    organismo = models.CharField(max_length=180, blank=True)
    enlace_oficial = models.URLField(blank=True)
    version_vigente = models.CharField(max_length=80, blank=True)
    activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
