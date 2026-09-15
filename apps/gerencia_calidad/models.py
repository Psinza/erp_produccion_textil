from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class NormaCalidad(models.Model):
    codigo = models.CharField(max_length=80, unique=True)
    titulo = models.CharField(max_length=200)
    clausula = models.CharField(max_length=80, blank=True)
    organismo = models.CharField(max_length=150, default='ISO')
    version = models.CharField(max_length=40, default='2015')
    enlace_oficial = models.URLField(blank=True)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.titulo}'


class ProcesoCalidad(models.Model):
    nombre = models.CharField(max_length=180, unique=True)
    objetivo = models.TextField()
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='procesos_calidad')
    entradas = models.TextField(blank=True)
    salidas = models.TextField(blank=True)
    indicadores = models.TextField(blank=True)
    riesgos = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class AuditoriaCalidadISO(models.Model):
    ESTADOS = [('planificada', 'Planificada'), ('en_ejecucion', 'En ejecución'), ('cerrada', 'Cerrada')]
    numero = models.CharField(max_length=30, unique=True)
    proceso = models.ForeignKey(ProcesoCalidad, on_delete=models.PROTECT, related_name='auditorias')
    norma = models.ForeignKey(NormaCalidad, on_delete=models.PROTECT, related_name='auditorias')
    auditor = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='auditorias_iso')
    fecha = models.DateField(default=timezone.localdate)
    alcance = models.TextField()
    resultado = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='planificada')

    def __str__(self):
        return f'{self.numero} - {self.proceso}'


class NoConformidad(models.Model):
    TIPOS = [('mayor', 'Mayor'), ('menor', 'Menor'), ('observacion', 'Observación')]
    ESTADOS = [('abierta', 'Abierta'), ('accion', 'En acción'), ('verificada', 'Verificada'), ('cerrada', 'Cerrada')]
    numero = models.CharField(max_length=30, unique=True)
    auditoria = models.ForeignKey(AuditoriaCalidadISO, on_delete=models.PROTECT, related_name='no_conformidades', null=True, blank=True)
    proceso = models.ForeignKey(ProcesoCalidad, on_delete=models.PROTECT, related_name='no_conformidades')
    tipo = models.CharField(max_length=12, choices=TIPOS)
    requisito = models.CharField(max_length=180)
    descripcion = models.TextField()
    causa = models.TextField(blank=True)
    accion_correctiva = models.TextField(blank=True)
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='no_conformidades')
    fecha = models.DateField(default=timezone.localdate)
    fecha_compromiso = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='abierta')

    def clean(self):
        if self.fecha_compromiso and self.fecha_compromiso < self.fecha:
            raise ValidationError({'fecha_compromiso': 'No puede ser anterior al registro.'})

    def __str__(self):
        return f'{self.numero} - {self.proceso}'


class IndicadorCalidad(models.Model):
    nombre = models.CharField(max_length=180)
    periodo = models.CharField(max_length=30)
    unidad = models.CharField(max_length=40)
    meta = models.DecimalField(max_digits=14, decimal_places=2)
    resultado = models.DecimalField(max_digits=14, decimal_places=2)
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='indicadores_calidad')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.nombre} - {self.periodo}'
