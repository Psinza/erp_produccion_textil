from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    tipo = models.CharField(max_length=80, default='Área')
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.nombre


class PersonalServicios(models.Model):
    ESTADOS = [('activo', 'Activo'), ('inactivo', 'Inactivo'), ('vacaciones', 'Vacaciones')]
    nombre_completo = models.CharField(max_length=180)
    cedula = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=120)
    especialidad = models.CharField(max_length=150, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='personal')
    telefono = models.CharField(max_length=30, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='activo')
    supervisor = models.CharField(max_length=180, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('nombre_completo',)
        verbose_name = 'Personal de servicios generales'
        verbose_name_plural = 'Personal de servicios generales'

    def __str__(self):
        return f'{self.nombre_completo} - {self.cargo}'


class TareaDiaria(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('en_ejecucion', 'En ejecución'), ('completada', 'Completada'), ('no_realizada', 'No realizada')]
    fecha = models.DateField(default=timezone.localdate)
    titulo = models.CharField(max_length=180)
    descripcion = models.TextField(blank=True)
    responsable = models.ForeignKey(PersonalServicios, on_delete=models.PROTECT, related_name='tareas')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='tareas')
    hora_programada = models.TimeField(null=True, blank=True)
    hora_ejecucion = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    evidencia = models.FileField(upload_to='servicios/tareas/%Y/%m/', blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('-fecha', 'hora_programada')

    def __str__(self):
        return f'{self.fecha:%d/%m/%Y} - {self.titulo}'


class PlanMantenimiento(models.Model):
    TIPOS = [('preventivo', 'Preventivo'), ('correctivo', 'Correctivo')]
    ESTADOS = [('solicitado', 'Solicitado'), ('programado', 'Programado'), ('en_ejecucion', 'En ejecución'), ('completado', 'Completado'), ('cancelado', 'Cancelado')]
    codigo = models.CharField(max_length=30, unique=True)
    tipo = models.CharField(max_length=12, choices=TIPOS)
    equipo_o_area = models.CharField(max_length=180)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='mantenimientos')
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, default='media')
    fecha_programada = models.DateField(null=True, blank=True)
    fecha_ejecucion = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(PersonalServicios, on_delete=models.PROTECT, related_name='mantenimientos')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='solicitado')
    costo_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('-fecha_programada', '-codigo')

    def __str__(self):
        return f'{self.codigo} - {self.equipo_o_area}'


class EquipoServicios(models.Model):
    ESTADOS = [('operativo', 'Operativo'), ('mantenimiento', 'En mantenimiento'), ('dañado', 'Dañado'), ('baja', 'Dado de baja')]
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    marca_modelo = models.CharField(max_length=150, blank=True)
    serial = models.CharField(max_length=100, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='equipos')
    custodio = models.ForeignKey(PersonalServicios, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipos_custodiados')
    fecha_adquisicion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='operativo')
    valor_referencial = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('categoria', 'nombre')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class SolicitudMaterial(models.Model):
    ESTADOS = [('solicitada', 'Solicitada'), ('aprobada', 'Aprobada'), ('entregada', 'Entregada'), ('rechazada', 'Rechazada'), ('anulada', 'Anulada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(PersonalServicios, on_delete=models.PROTECT, related_name='solicitudes_material')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='solicitudes_material')
    material = models.CharField(max_length=180)
    cantidad = models.DecimalField(max_digits=14, decimal_places=3)
    unidad = models.CharField(max_length=30)
    justificacion = models.TextField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitada')
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='materiales_aprobados')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': 'La cantidad debe ser mayor que cero.'})

    def __str__(self):
        return f'{self.numero} - {self.material}'


class SolicitudServicio(models.Model):
    TIPOS = [('interno', 'Servicio interno'), ('contratista', 'Contratista'), ('emergencia', 'Emergencia')]
    ESTADOS = [('solicitada', 'Solicitada'), ('aprobada', 'Aprobada'), ('asignada', 'Asignada'), ('en_ejecucion', 'En ejecución'), ('completada', 'Completada'), ('rechazada', 'Rechazada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(PersonalServicios, on_delete=models.PROTECT, related_name='solicitudes_servicio')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='solicitudes_servicio')
    tipo = models.CharField(max_length=15, choices=TIPOS, default='interno')
    servicio_requerido = models.CharField(max_length=180)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, default='media')
    fecha_requerida = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='solicitada')
    responsable = models.ForeignKey(PersonalServicios, on_delete=models.PROTECT, null=True, blank=True, related_name='servicios_asignados')
    costo_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.numero} - {self.servicio_requerido}'
