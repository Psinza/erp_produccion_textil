from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class PlanAuditoria(models.Model):
    ESTADOS = [('borrador', 'Borrador'), ('aprobado', 'Aprobado'), ('en_ejecucion', 'En ejecución'), ('cerrado', 'Cerrado')]
    nombre = models.CharField(max_length=180)
    ejercicio = models.PositiveIntegerField()
    alcance = models.TextField()
    objetivo = models.TextField()
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='planes_auditoria')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='borrador')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'No puede ser anterior a la fecha de inicio.'})

    def __str__(self):
        return f'{self.ejercicio} - {self.nombre}'


class HallazgoAuditoria(models.Model):
    TIPOS = [('no_conformidad_mayor', 'No conformidad mayor'), ('no_conformidad_menor', 'No conformidad menor'), ('observacion', 'Observación'), ('oportunidad', 'Oportunidad de mejora')]
    ESTADOS = [('abierto', 'Abierto'), ('plan_accion', 'En plan de acción'), ('verificado', 'Verificado'), ('cerrado', 'Cerrado')]
    plan = models.ForeignKey(PlanAuditoria, on_delete=models.PROTECT, related_name='hallazgos')
    codigo = models.CharField(max_length=30)
    proceso = models.CharField(max_length=150)
    tipo = models.CharField(max_length=25, choices=TIPOS)
    descripcion = models.TextField()
    criterio = models.TextField(blank=True)
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='hallazgos_auditoria')
    fecha = models.DateField(default=timezone.localdate)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='abierto')
    fecha_cierre = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('plan', 'codigo')

    def clean(self):
        if self.fecha_cierre and self.fecha_cierre < self.fecha:
            raise ValidationError({'fecha_cierre': 'No puede ser anterior al hallazgo.'})

    def __str__(self):
        return f'{self.codigo} - {self.proceso}'


class AccionCorrectiva(models.Model):
    hallazgo = models.ForeignKey(HallazgoAuditoria, on_delete=models.PROTECT, related_name='acciones')
    accion = models.TextField()
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='acciones_correctivas')
    fecha_compromiso = models.DateField()
    fecha_cierre = models.DateField(null=True, blank=True)
    evidencia = models.FileField(upload_to='auditoria/evidencias/%Y/%m/', blank=True)
    verificada = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.fecha_cierre and self.fecha_cierre < self.fecha_compromiso:
            raise ValidationError({'fecha_cierre': 'No puede ser anterior a la fecha compromiso.'})

    def __str__(self):
        return f'{self.hallazgo.codigo} - acción correctiva'


class NormaAuditoria(models.Model):
    codigo = models.CharField(max_length=80, unique=True)
    titulo = models.CharField(max_length=180)
    organismo = models.CharField(max_length=150)
    jurisdiccion = models.CharField(max_length=80, default='Venezuela')
    version = models.CharField(max_length=40, blank=True)
    enlace_oficial = models.URLField(blank=True)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.titulo}'
