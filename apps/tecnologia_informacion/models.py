from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PersonalTI(models.Model):
    ESTADOS = [('activo', 'Activo'), ('inactivo', 'Inactivo'), ('vacaciones', 'Vacaciones')]
    nombre_completo = models.CharField(max_length=180)
    cedula = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=120)
    especialidad = models.CharField(max_length=150, blank=True)
    ubicacion = models.CharField(max_length=150, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='activo')
    supervisor = models.CharField(max_length=180, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('nombre_completo',)
        verbose_name = 'Personal de tecnología'
        verbose_name_plural = 'Personal de tecnología'

    def __str__(self):
        return f'{self.nombre_completo} - {self.cargo}'


class TicketTI(models.Model):
    PRIORIDADES = [('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('critica', 'Crítica')]
    ESTADOS = [('abierto', 'Abierto'), ('asignado', 'Asignado'), ('en_atencion', 'En atención'), ('resuelto', 'Resuelto'), ('cerrado', 'Cerrado'), ('cancelado', 'Cancelado')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    solicitante = models.CharField(max_length=180)
    area_solicitante = models.CharField(max_length=150, blank=True)
    asunto = models.CharField(max_length=180)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100, default='Soporte')
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='abierto')
    asignado_a = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, null=True, blank=True, related_name='tickets')
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    solucion = models.TextField(blank=True)

    class Meta:
        ordering = ('-fecha',)

    def clean(self):
        if self.fecha_vencimiento and self.fecha_vencimiento < self.fecha:
            raise ValidationError({'fecha_vencimiento': 'No puede ser anterior a la fecha de creación.'})
        if self.fecha_resolucion and self.fecha_resolucion < self.fecha:
            raise ValidationError({'fecha_resolucion': 'No puede ser anterior a la fecha de creación.'})

    def __str__(self):
        return f'{self.numero} - {self.asunto}'


class MonitoreoRed(models.Model):
    ESTADOS = [('operativo', 'Operativo'), ('degradado', 'Degradado'), ('caido', 'Caído'), ('mantenimiento', 'Mantenimiento')]
    fecha = models.DateTimeField(default=timezone.now)
    servicio_o_enlace = models.CharField(max_length=180)
    segmento = models.CharField(max_length=120, blank=True)
    direccion = models.GenericIPAddressField(null=True, blank=True)
    latencia_ms = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    disponibilidad = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('100.00'))
    estado = models.CharField(max_length=15, choices=ESTADOS, default='operativo')
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='monitoreos')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if not 0 <= self.disponibilidad <= 100:
            raise ValidationError({'disponibilidad': 'Debe estar entre 0 y 100.'})
        if self.latencia_ms is not None and self.latencia_ms < 0:
            raise ValidationError({'latencia_ms': 'No puede ser negativa.'})

    def __str__(self):
        return f'{self.servicio_o_enlace} - {self.estado}'


class AsignacionDiaria(models.Model):
    ESTADOS = [('planificada', 'Planificada'), ('en_ejecucion', 'En ejecución'), ('completada', 'Completada'), ('no_realizada', 'No realizada')]
    fecha = models.DateField(default=timezone.localdate)
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='asignaciones')
    actividad = models.CharField(max_length=180)
    prioridad = models.CharField(max_length=10, choices=TicketTI.PRIORIDADES, default='media')
    ubicacion = models.CharField(max_length=150, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='planificada')
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('-fecha',)

    def __str__(self):
        return f'{self.fecha:%d/%m/%Y} - {self.actividad}'


class EquipoTI(models.Model):
    TIPOS = [('computador', 'Computador'), ('servidor', 'Servidor'), ('red', 'Equipo de red'), ('impresora', 'Impresora'), ('telefonia', 'Telefonía'), ('otro', 'Otro')]
    ESTADOS = [('operativo', 'Operativo'), ('asignado', 'Asignado'), ('mantenimiento', 'En mantenimiento'), ('dañado', 'Dañado'), ('baja', 'Dado de baja')]
    codigo = models.CharField(max_length=40, unique=True)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    nombre = models.CharField(max_length=150)
    marca_modelo = models.CharField(max_length=150, blank=True)
    serial = models.CharField(max_length=100, blank=True)
    ubicacion = models.CharField(max_length=150, blank=True)
    custodio = models.CharField(max_length=180, blank=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    garantia_hasta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='operativo')
    valor_referencial = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.valor_referencial < 0:
            raise ValidationError({'valor_referencial': 'No puede ser negativo.'})

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class MantenimientoEquipo(models.Model):
    TIPOS = [('preventivo', 'Preventivo'), ('correctivo', 'Correctivo')]
    ESTADOS = [('solicitado', 'Solicitado'), ('programado', 'Programado'), ('en_ejecucion', 'En ejecución'), ('completado', 'Completado'), ('cancelado', 'Cancelado')]
    codigo = models.CharField(max_length=30, unique=True)
    equipo = models.ForeignKey(EquipoTI, on_delete=models.PROTECT, related_name='mantenimientos')
    tipo = models.CharField(max_length=12, choices=TIPOS)
    descripcion = models.TextField()
    fecha_programada = models.DateField(null=True, blank=True)
    fecha_ejecucion = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='mantenimientos')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='solicitado')
    costo_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.costo_estimado < 0 or self.costo_real < 0:
            raise ValidationError('Los costos no pueden ser negativos.')
        if self.fecha_programada and self.fecha_ejecucion and self.fecha_ejecucion < self.fecha_programada:
            raise ValidationError({'fecha_ejecucion': 'No puede ser anterior a la fecha programada.'})

    def __str__(self):
        return f'{self.codigo} - {self.equipo}'


class PlanTrabajoTI(models.Model):
    ESTADOS = [('borrador', 'Borrador'), ('aprobado', 'Aprobado'), ('en_ejecucion', 'En ejecución'), ('cerrado', 'Cerrado')]
    nombre = models.CharField(max_length=180)
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    objetivo = models.TextField()
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='planes_trabajo')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='borrador')
    avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.periodo_fin < self.periodo_inicio:
            raise ValidationError({'periodo_fin': 'Debe ser posterior o igual al inicio.'})
        if not 0 <= self.avance <= 100:
            raise ValidationError({'avance': 'Debe estar entre 0 y 100.'})

    def __str__(self):
        return self.nombre


class SolicitudEquipo(models.Model):
    ESTADOS = [('solicitada', 'Solicitada'), ('evaluacion', 'En evaluación'), ('aprobada', 'Aprobada'), ('entregada', 'Entregada'), ('rechazada', 'Rechazada'), ('anulada', 'Anulada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    solicitante = models.CharField(max_length=180)
    area = models.CharField(max_length=150)
    equipo_requerido = models.CharField(max_length=180)
    cantidad = models.PositiveIntegerField(default=1)
    justificacion = models.TextField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitada')
    aprobado_por = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, null=True, blank=True, related_name='solicitudes_aprobadas')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': 'Debe ser mayor que cero.'})

    def __str__(self):
        return f'{self.numero} - {self.equipo_requerido}'


class RecepcionEquipo(models.Model):
    numero_acta = models.CharField(max_length=30, unique=True)
    fecha = models.DateField(default=timezone.localdate)
    equipo = models.ForeignKey(EquipoTI, on_delete=models.PROTECT, related_name='recepciones')
    proveedor = models.CharField(max_length=180, blank=True)
    documento_compra = models.CharField(max_length=80, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    recibido_por = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='recepciones')
    conforme = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': 'Debe ser mayor que cero.'})

    def __str__(self):
        return f'{self.numero_acta} - {self.equipo}'


class IndicadorGestion(models.Model):
    nombre = models.CharField(max_length=180)
    periodo = models.CharField(max_length=30)
    unidad = models.CharField(max_length=40)
    meta = models.DecimalField(max_digits=14, decimal_places=2)
    resultado = models.DecimalField(max_digits=14, decimal_places=2)
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='indicadores')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.nombre} - {self.periodo}'


class ServicioTI(models.Model):
    ESTADOS = [('activo', 'Activo'), ('apagado', 'Apagado'), ('mantenimiento', 'Mantenimiento'), ('retirado', 'Retirado')]
    nombre = models.CharField(max_length=180, unique=True)
    tipo = models.CharField(max_length=100)
    ambiente = models.CharField(max_length=80, default='Producción')
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='servicios')
    ubicacion = models.CharField(max_length=150, blank=True)
    fecha_alta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='activo')
    criticidad = models.CharField(max_length=20, default='media')
    dependencia = models.CharField(max_length=180, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.nombre} - {self.estado}'


class PlanModernizacion(models.Model):
    ESTADOS = [('propuesto', 'Propuesto'), ('aprobado', 'Aprobado'), ('en_ejecucion', 'En ejecución'), ('completado', 'Completado'), ('detenido', 'Detenido')]
    nombre = models.CharField(max_length=180)
    alcance = models.TextField()
    justificacion = models.TextField()
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(PersonalTI, on_delete=models.PROTECT, related_name='modernizaciones')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='propuesto')
    avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    presupuesto_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'No puede ser anterior al inicio.'})
        if not 0 <= self.avance <= 100:
            raise ValidationError({'avance': 'Debe estar entre 0 y 100.'})
        if self.presupuesto_estimado < 0:
            raise ValidationError({'presupuesto_estimado': 'No puede ser negativo.'})

    def __str__(self):
        return self.nombre
