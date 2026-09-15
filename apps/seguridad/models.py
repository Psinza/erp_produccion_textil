from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PuestoSeguridad(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'Puesto de seguridad'
        verbose_name_plural = 'Puestos de seguridad'

    def __str__(self):
        return f'{self.nombre} - {self.ubicacion}'


class Guardia(models.Model):
    ESTADOS = [('activo', 'Activo'), ('inactivo', 'Inactivo'), ('suspendido', 'Suspendido')]
    nombre_completo = models.CharField(max_length=180)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    empresa = models.CharField(max_length=180, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='activo')
    fecha_ingreso = models.DateField(null=True, blank=True)
    capacitacion_vigente_hasta = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('nombre_completo',)
        verbose_name = 'Guardia de seguridad'
        verbose_name_plural = 'Guardias de seguridad'

    def __str__(self):
        return f'{self.nombre_completo} ({self.cedula})'

    @property
    def capacitacion_vigente(self):
        return bool(self.capacitacion_vigente_hasta and self.capacitacion_vigente_hasta >= timezone.localdate())


class TurnoGuardia(models.Model):
    guardia = models.ForeignKey(Guardia, on_delete=models.PROTECT, related_name='turnos')
    puesto = models.ForeignKey(PuestoSeguridad, on_delete=models.PROTECT, related_name='turnos')
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    patron = models.CharField(max_length=20, default='24x72', editable=False)
    relevo_realizado = models.BooleanField(default=False)
    novedades = models.TextField(blank=True)

    class Meta:
        ordering = ('-inicio',)
        verbose_name = 'Turno de guardia'
        verbose_name_plural = 'Turnos de guardia'

    def clean(self):
        if self.fin <= self.inicio:
            raise ValidationError({'fin': 'El fin del turno debe ser posterior al inicio.'})
        if self.fin - self.inicio != timedelta(hours=24):
            raise ValidationError({'fin': 'El turno operativo 24x72 debe durar exactamente 24 horas.'})

    def __str__(self):
        return f'{self.guardia} - {self.puesto} - {self.inicio:%d/%m/%Y %H:%M}'


class EquipoSeguridad(models.Model):
    TIPOS = [('uniforme', 'Uniforme'), ('epp', 'EPP'), ('comunicacion', 'Comunicación'), ('defensa', 'Defensa autorizada'), ('otro', 'Otro')]
    nombre = models.CharField(max_length=140)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    codigo_interno = models.CharField(max_length=50, unique=True)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    requiere_vencimiento = models.BooleanField(default=False)
    especificacion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('tipo', 'nombre')
        verbose_name = 'Equipo de seguridad'
        verbose_name_plural = 'Equipos de seguridad'

    def __str__(self):
        return f'{self.nombre} [{self.codigo_interno}]'


class DotacionEquipo(models.Model):
    ESTADOS = [('entregado', 'Entregado'), ('devuelto', 'Devuelto'), ('perdido', 'Reportado perdido'), ('mantenimiento', 'En mantenimiento')]
    guardia = models.ForeignKey(Guardia, on_delete=models.PROTECT, related_name='dotaciones')
    equipo = models.ForeignKey(EquipoSeguridad, on_delete=models.PROTECT, related_name='dotaciones')
    cantidad = models.PositiveIntegerField(default=1)
    fecha_entrega = models.DateField(default=timezone.localdate)
    fecha_devolucion = models.DateField(null=True, blank=True)
    vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=16, choices=ESTADOS, default='entregado')
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.fecha_devolucion and self.fecha_devolucion < self.fecha_entrega:
            raise ValidationError({'fecha_devolucion': 'No puede ser anterior a la entrega.'})
        if self.equipo_id and self.cantidad < 1:
            raise ValidationError({'cantidad': 'La cantidad debe ser mayor que cero.'})


class PaseIngreso(models.Model):
    TIPOS = [('visitante', 'Visitante'), ('contratista', 'Contratista'), ('proveedor', 'Proveedor'), ('empleado', 'Empleado'), ('vehiculo', 'Vehículo')]
    ESTADOS = [('solicitado', 'Solicitado'), ('autorizado', 'Autorizado'), ('usado', 'Usado'), ('anulado', 'Anulado'), ('vencido', 'Vencido')]
    codigo = models.CharField(max_length=30, unique=True)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    nombre_visitante = models.CharField(max_length=180)
    documento = models.CharField(max_length=30, blank=True)
    empresa = models.CharField(max_length=180, blank=True)
    motivo = models.CharField(max_length=250)
    persona_responsable = models.CharField(max_length=180, blank=True)
    fecha_desde = models.DateTimeField()
    fecha_hasta = models.DateTimeField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitado')
    placa = models.CharField(max_length=20, blank=True)
    observaciones = models.TextField(blank=True)
    autorizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pases_autorizados')

    def clean(self):
        if self.fecha_hasta <= self.fecha_desde:
            raise ValidationError({'fecha_hasta': 'La vigencia final debe ser posterior a la inicial.'})

    def __str__(self):
        return f'{self.codigo} - {self.nombre_visitante}'


class RegistroAcceso(models.Model):
    TIPOS = [('ingreso', 'Ingreso'), ('salida', 'Salida'), ('rechazo', 'Acceso rechazado')]
    pase = models.ForeignKey(PaseIngreso, on_delete=models.PROTECT, null=True, blank=True, related_name='registros')
    puesto = models.ForeignKey(PuestoSeguridad, on_delete=models.PROTECT, related_name='registros_acceso')
    fecha_hora = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    persona = models.CharField(max_length=180)
    documento = models.CharField(max_length=30, blank=True)
    placa = models.CharField(max_length=20, blank=True)
    notificado_a = models.CharField(max_length=180, blank=True)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='registros_acceso')

    class Meta:
        ordering = ('-fecha_hora',)


class OrdenSalidaMaterial(models.Model):
    ESTADOS = [('solicitada', 'Solicitada'), ('autorizada', 'Autorizada'), ('verificada', 'Verificada'), ('anulada', 'Anulada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    solicitante = models.CharField(max_length=180)
    destino = models.CharField(max_length=200)
    placa = models.CharField(max_length=20, blank=True)
    conductor = models.CharField(max_length=180, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitada')
    observaciones = models.TextField(blank=True)
    autorizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('-fecha',)

    def __str__(self):
        return self.numero


class MaterialSalida(models.Model):
    orden = models.ForeignKey(OrdenSalidaMaterial, on_delete=models.CASCADE, related_name='materiales')
    descripcion = models.CharField(max_length=250)
    cantidad = models.DecimalField(max_digits=14, decimal_places=3)
    unidad = models.CharField(max_length=20)
    lote = models.CharField(max_length=80, blank=True)
    verificado = models.BooleanField(default=False)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': 'La cantidad debe ser mayor que cero.'})


class RondaSeguridad(models.Model):
    ESTADOS = [('iniciada', 'Iniciada'), ('completada', 'Completada'), ('con_novedad', 'Con novedad')]
    turno = models.ForeignKey(TurnoGuardia, on_delete=models.PROTECT, related_name='rondas')
    fecha_hora = models.DateTimeField(default=timezone.now)
    galpon = models.CharField(max_length=120)
    puntos_verificados = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='iniciada')
    hallazgos = models.TextField(blank=True)


class IncidenteSeguridad(models.Model):
    TIPOS = [('intrusion', 'Intrusión'), ('accidente', 'Accidente'), ('incendio', 'Incendio'), ('derrame', 'Derrame'), ('robo', 'Pérdida o robo'), ('otro', 'Otro')]
    SEVERIDADES = [('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('critica', 'Crítica')]
    ESTADOS = [('abierto', 'Abierto'), ('investigacion', 'En investigación'), ('cerrado', 'Cerrado')]
    codigo = models.CharField(max_length=30, unique=True)
    fecha_hora = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    severidad = models.CharField(max_length=10, choices=SEVERIDADES, default='media')
    ubicacion = models.CharField(max_length=180)
    descripcion = models.TextField()
    acciones_inmediatas = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='abierto')
    reportado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='incidentes_reportados')
    responsable = models.CharField(max_length=180, blank=True)
    cerrado_en = models.DateTimeField(null=True, blank=True)


class InspeccionSST(models.Model):
    ESTADOS = [('planificada', 'Planificada'), ('ejecutada', 'Ejecutada'), ('con_hallazgos', 'Con hallazgos'), ('cerrada', 'Cerrada')]
    fecha = models.DateField(default=timezone.localdate)
    area = models.CharField(max_length=180)
    inspector = models.CharField(max_length=180)
    referencia_normativa = models.CharField(max_length=250, blank=True)
    hallazgos = models.TextField(blank=True)
    acciones_correctivas = models.TextField(blank=True)
    fecha_compromiso = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='planificada')


class NormaReferencia(models.Model):
    jurisdiccion = models.CharField(max_length=80, default='Venezuela')
    codigo = models.CharField(max_length=80, unique=True)
    nombre = models.CharField(max_length=250)
    ambito = models.CharField(max_length=120, help_text='Seguridad industrial, SST, control de acceso, etc.')
    organismo = models.CharField(max_length=180, blank=True)
    version_vigente = models.CharField(max_length=60, blank=True)
    enlace_oficial = models.URLField(blank=True)
    activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('jurisdiccion', 'codigo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
