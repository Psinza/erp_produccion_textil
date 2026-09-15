from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PersonalMedico(models.Model):
    empleado = models.OneToOneField('rrhh.Empleado', on_delete=models.PROTECT, related_name='perfil_medico')
    especialidad = models.CharField(max_length=150)
    registro_profesional = models.CharField(max_length=80, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.empleado.nombre_completo} - {self.especialidad}'


class PresupuestoMedico(models.Model):
    ejercicio = models.PositiveIntegerField()
    partida = models.CharField(max_length=120)
    monto_aprobado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monto_comprometido = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monto_ejecutado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    responsable = models.ForeignKey(PersonalMedico, on_delete=models.PROTECT, related_name='presupuestos')

    class Meta:
        unique_together = ('ejercicio', 'partida')

    def clean(self):
        if min(self.monto_aprobado, self.monto_comprometido, self.monto_ejecutado) < 0:
            raise ValidationError('Los montos no pueden ser negativos.')
        if self.monto_comprometido > self.monto_aprobado:
            raise ValidationError({'monto_comprometido': 'No puede superar el aprobado.'})
        if self.monto_ejecutado > self.monto_comprometido:
            raise ValidationError({'monto_ejecutado': 'No puede superar el comprometido.'})

    def __str__(self):
        return f'{self.ejercicio} - {self.partida}'


class ResultadoIngreso(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('apto', 'Apto'), ('no_apto', 'No apto'), ('observado', 'Observado')]
    empleado = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='resultados_ingreso')
    fecha = models.DateField(default=timezone.localdate)
    tipo_examen = models.CharField(max_length=150)
    resultado = models.TextField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default='pendiente')
    profesional = models.ForeignKey(PersonalMedico, on_delete=models.PROTECT, related_name='resultados_ingreso')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.empleado.nombre_completo} - {self.tipo_examen}'


class ReposoMedico(models.Model):
    ESTADOS = [('solicitado', 'Solicitado'), ('validado', 'Validado'), ('rechazado', 'Rechazado'), ('cerrado', 'Cerrado')]
    empleado = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='reposos_medicos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    diagnostico = models.TextField()
    soporte = models.FileField(upload_to='medico/reposos/%Y/%m/', blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='solicitado')
    validado_por = models.ForeignKey(PersonalMedico, on_delete=models.PROTECT, null=True, blank=True, related_name='reposos_validados')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'Debe ser posterior o igual al inicio.'})

    def __str__(self):
        return f'{self.empleado.nombre_completo} - {self.fecha_inicio:%d/%m/%Y}'


class AfectacionPersonal(models.Model):
    ESTADOS = [('abierta', 'Abierta'), ('en_seguimiento', 'En seguimiento'), ('cerrada', 'Cerrada')]
    empleado = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='afectaciones_salud')
    fecha = models.DateField(default=timezone.localdate)
    tipo = models.CharField(max_length=120)
    descripcion = models.TextField()
    restricciones = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='abierta')
    profesional = models.ForeignKey(PersonalMedico, on_delete=models.PROTECT, related_name='afectaciones')
    confidencial = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.empleado.nombre_completo} - {self.tipo}'


class EquipoMedico(models.Model):
    ESTADOS = [('operativo', 'Operativo'), ('asignado', 'Asignado'), ('mantenimiento', 'En mantenimiento'), ('dañado', 'Dañado'), ('baja', 'Dado de baja')]
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=150)
    marca_modelo = models.CharField(max_length=150, blank=True)
    serial = models.CharField(max_length=100, blank=True)
    ubicacion = models.CharField(max_length=150)
    custodio = models.ForeignKey(PersonalMedico, on_delete=models.PROTECT, related_name='equipos')
    fecha_adquisicion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='operativo')
    valor_referencial = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    partida = models.ForeignKey(PresupuestoMedico, on_delete=models.PROTECT, related_name='equipos')
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.valor_referencial < 0:
            raise ValidationError({'valor_referencial': 'No puede ser negativo.'})

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
