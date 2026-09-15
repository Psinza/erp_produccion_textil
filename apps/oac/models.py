from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PersonalOAC(models.Model):
    empleado = models.OneToOneField('rrhh.Empleado', on_delete=models.PROTECT, related_name='perfil_oac')
    funcion = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.empleado.nombre_completo} - {self.funcion}'


class PresupuestoOAC(models.Model):
    ejercicio = models.PositiveIntegerField()
    partida = models.CharField(max_length=120)
    monto_aprobado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monto_comprometido = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monto_ejecutado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    responsable = models.ForeignKey(PersonalOAC, on_delete=models.PROTECT, related_name='presupuestos')

    class Meta:
        unique_together = ('ejercicio', 'partida')
        ordering = ('-ejercicio', 'partida')

    def clean(self):
        if min(self.monto_aprobado, self.monto_comprometido, self.monto_ejecutado) < 0:
            raise ValidationError('Los montos presupuestarios no pueden ser negativos.')
        if self.monto_comprometido > self.monto_aprobado:
            raise ValidationError({'monto_comprometido': 'No puede superar el monto aprobado.'})
        if self.monto_ejecutado > self.monto_comprometido:
            raise ValidationError({'monto_ejecutado': 'No puede superar el monto comprometido.'})

    def __str__(self):
        return f'{self.ejercicio} - {self.partida}'


class Donacion(models.Model):
    ESTADOS = [('solicitada', 'Solicitada'), ('aprobada', 'Aprobada'), ('entregada', 'Entregada'), ('rechazada', 'Rechazada'), ('anulada', 'Anulada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    beneficiario = models.CharField(max_length=180)
    cedula = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=120)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField(default=1)
    monto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    partida = models.ForeignKey(PresupuestoOAC, on_delete=models.PROTECT, related_name='donaciones')
    responsable = models.ForeignKey(PersonalOAC, on_delete=models.PROTECT, related_name='donaciones')
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitada')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.cantidad <= 0 or self.monto < 0:
            raise ValidationError('La cantidad debe ser mayor que cero y el monto no puede ser negativo.')

    def __str__(self):
        return f'{self.numero} - {self.beneficiario}'


class CitaCiudadana(models.Model):
    ESTADOS = [('solicitada', 'Solicitada'), ('confirmada', 'Confirmada'), ('atendida', 'Atendida'), ('no_asistio', 'No asistió'), ('cancelada', 'Cancelada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    ciudadano = models.CharField(max_length=180)
    cedula = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    motivo = models.TextField()
    fecha_cita = models.DateTimeField()
    responsable = models.ForeignKey(PersonalOAC, on_delete=models.PROTECT, related_name='citas')
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitada')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.fecha_cita < self.fecha_solicitud:
            raise ValidationError({'fecha_cita': 'No puede ser anterior a la solicitud.'})

    def __str__(self):
        return f'{self.numero} - {self.ciudadano}'


class BusquedaMedicamento(models.Model):
    ESTADOS = [('recibida', 'Recibida'), ('en_busqueda', 'En búsqueda'), ('encontrada', 'Encontrada'), ('no_disponible', 'No disponible'), ('cerrada', 'Cerrada')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(default=timezone.now)
    solicitante = models.CharField(max_length=180)
    cedula = models.CharField(max_length=20, blank=True)
    medicamento = models.CharField(max_length=180)
    presentacion = models.CharField(max_length=120, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='recibida')
    responsable = models.ForeignKey(PersonalOAC, on_delete=models.PROTECT, related_name='busquedas_medicamentos')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': 'Debe ser mayor que cero.'})

    def __str__(self):
        return f'{self.numero} - {self.medicamento}'


class JornadaMedica(models.Model):
    ESTADOS = [('planificada', 'Planificada'), ('convocada', 'Convocada'), ('ejecutada', 'Ejecutada'), ('cancelada', 'Cancelada')]
    nombre = models.CharField(max_length=180)
    fecha = models.DateField()
    especialidad = models.CharField(max_length=120)
    lugar = models.CharField(max_length=150)
    capacidad = models.PositiveIntegerField(default=1)
    atendidos = models.PositiveIntegerField(default=0)
    responsable = models.ForeignKey(PersonalOAC, on_delete=models.PROTECT, related_name='jornadas')
    estado = models.CharField(max_length=12, choices=ESTADOS, default='planificada')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.atendidos > self.capacidad:
            raise ValidationError({'atendidos': 'No puede superar la capacidad.'})

    def __str__(self):
        return f'{self.nombre} - {self.fecha:%d/%m/%Y}'
