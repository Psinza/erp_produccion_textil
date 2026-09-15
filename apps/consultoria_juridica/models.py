from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class CasoJuridico(models.Model):
    ESTADOS = [('recibido', 'Recibido'), ('en_analisis', 'En análisis'), ('en_tramite', 'En trámite'), ('cerrado', 'Cerrado'), ('archivado', 'Archivado')]
    numero = models.CharField(max_length=30, unique=True)
    fecha = models.DateField(default=timezone.localdate)
    asunto = models.CharField(max_length=180)
    area_solicitante = models.CharField(max_length=150)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=15, default='media')
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='casos_juridicos')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='recibido')
    fecha_limite = models.DateField(null=True, blank=True)
    confidencial = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.fecha_limite and self.fecha_limite < self.fecha:
            raise ValidationError({'fecha_limite': 'No puede ser anterior a la recepción.'})

    def __str__(self):
        return f'{self.numero} - {self.asunto}'


class DictamenJuridico(models.Model):
    caso = models.ForeignKey(CasoJuridico, on_delete=models.PROTECT, related_name='dictamenes')
    fecha = models.DateField(default=timezone.localdate)
    asunto = models.CharField(max_length=180)
    fundamentos = models.TextField()
    recomendacion = models.TextField()
    emitido_por = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='dictamenes_juridicos')
    aprobado = models.BooleanField(default=False)
    documento = models.FileField(upload_to='juridica/dictamenes/%Y/%m/', blank=True)

    def __str__(self):
        return f'{self.caso.numero} - {self.asunto}'


class NormaLegal(models.Model):
    codigo = models.CharField(max_length=80, unique=True)
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    organismo = models.CharField(max_length=150)
    jurisdiccion = models.CharField(max_length=80, default='Venezuela')
    fecha_vigencia = models.DateField(null=True, blank=True)
    enlace_oficial = models.URLField(blank=True)
    vigente = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.codigo} - {self.titulo}'


class ContratoJuridico(models.Model):
    ESTADOS = [('borrador', 'Borrador'), ('revision', 'En revisión'), ('vigente', 'Vigente'), ('vencido', 'Vencido'), ('rescindido', 'Rescindido')]
    numero = models.CharField(max_length=40, unique=True)
    objeto = models.CharField(max_length=200)
    contraparte = models.CharField(max_length=180)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey('rrhh.Empleado', on_delete=models.PROTECT, related_name='contratos_juridicos')
    monto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='borrador')
    documento = models.FileField(upload_to='juridica/contratos/%Y/%m/', blank=True)

    def clean(self):
        if self.monto < 0:
            raise ValidationError({'monto': 'No puede ser negativo.'})
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'No puede ser anterior al inicio.'})

    def __str__(self):
        return f'{self.numero} - {self.objeto}'
