from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Proveedor(models.Model):
    ESTADOS = [('activo', 'Activo'), ('inhabilitado', 'Inhabilitado'), ('suspendido', 'Suspendido')]
    rif = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=220)
    domicilio = models.CharField(max_length=250, blank=True)
    contacto = models.CharField(max_length=180, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    registro_proveedores = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='activo')
    documentos_vigentes = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('razon_social',)

    def __str__(self):
        return f'{self.razon_social} ({self.rif})'


class ProcesoContratacion(models.Model):
    MODALIDADES = [('concurso_abierto', 'Concurso abierto'), ('consulta_precios', 'Consulta de precios'), ('contratacion_directa', 'Contratación directa'), ('contratacion_excluida', 'Contratación excluida')]
    ESTADOS = [('planificado', 'Planificado'), ('publicado', 'Publicado'), ('evaluacion', 'En evaluación'), ('adjudicado', 'Adjudicado'), ('contratado', 'Contratado'), ('ejecucion', 'En ejecución'), ('cerrado', 'Cerrado'), ('anulado', 'Anulado')]
    numero = models.CharField(max_length=40, unique=True)
    objeto = models.CharField(max_length=250)
    justificacion = models.TextField()
    unidad_solicitante = models.CharField(max_length=180)
    modalidad = models.CharField(max_length=25, choices=MODALIDADES)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='planificado')
    presupuesto_referencial = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    responsable = models.CharField(max_length=180)
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='procesos_contratacion_aprobados')
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ('-fecha_inicio', '-numero')

    def clean(self):
        if self.presupuesto_referencial < 0:
            raise ValidationError({'presupuesto_referencial': 'No puede ser negativo.'})
        if self.fecha_inicio and self.fecha_cierre and self.fecha_cierre < self.fecha_inicio:
            raise ValidationError({'fecha_cierre': 'No puede ser anterior a la fecha de inicio.'})

    def __str__(self):
        return f'{self.numero} - {self.objeto}'


class OfertaProveedor(models.Model):
    ESTADOS = [('recibida', 'Recibida'), ('evaluada', 'Evaluada'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')]
    proceso = models.ForeignKey(ProcesoContratacion, on_delete=models.CASCADE, related_name='ofertas')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='ofertas')
    fecha_recepcion = models.DateField(default=timezone.localdate)
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    plazo_dias = models.PositiveIntegerField(default=0)
    puntaje_tecnico = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    puntaje_economico = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='recibida')
    documento = models.FileField(upload_to='contrataciones/ofertas/%Y/%m/', blank=True)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.monto < 0:
            raise ValidationError({'monto': 'El monto no puede ser negativo.'})


class EvaluacionContratacion(models.Model):
    proceso = models.OneToOneField(ProcesoContratacion, on_delete=models.CASCADE, related_name='evaluacion')
    fecha = models.DateField(default=timezone.localdate)
    comite_o_responsable = models.CharField(max_length=220)
    metodologia = models.TextField()
    proveedor_recomendado = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True)
    acta_numero = models.CharField(max_length=60, blank=True)
    decision = models.TextField()
    documento = models.FileField(upload_to='contrataciones/evaluaciones/%Y/%m/', blank=True)


class Contrato(models.Model):
    ESTADOS = [('borrador', 'Borrador'), ('vigente', 'Vigente'), ('suspendido', 'Suspendido'), ('terminado', 'Terminado'), ('rescindido', 'Rescindido')]
    numero = models.CharField(max_length=50, unique=True)
    proceso = models.OneToOneField(ProcesoContratacion, on_delete=models.PROTECT, related_name='contrato')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='contratos')
    objeto = models.CharField(max_length=250)
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    fecha_firma = models.DateField(null=True, blank=True)
    inicio = models.DateField(null=True, blank=True)
    fin = models.DateField(null=True, blank=True)
    supervisor = models.CharField(max_length=180)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='borrador')
    documento = models.FileField(upload_to='contrataciones/contratos/%Y/%m/', blank=True)
    observaciones = models.TextField(blank=True)

    def clean(self):
        if self.inicio and self.fin and self.fin < self.inicio:
            raise ValidationError({'fin': 'No puede ser anterior al inicio.'})


class NormaContratacion(models.Model):
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
