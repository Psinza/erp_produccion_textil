from django.db import models
from django.conf import settings
from uuid import uuid4
from apps.produccion.models import ProductoTerminado

class CategoriaComercial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.FileField(upload_to='comercial/categorias/', null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías Comerciales"

class InformacionComercial(models.Model):
    """Información extendida del producto para el catálogo (Marketing)"""
    producto = models.OneToOneField(ProductoTerminado, on_delete=models.CASCADE, related_name='info_comercial')
    categoria = models.ForeignKey(CategoriaComercial, on_delete=models.SET_NULL, null=True, related_name='productos')
    nombre_comercial = models.CharField(max_length=255)
    descripcion_larga = models.TextField(help_text="Descripción detallada para catálogos o web")
    ficha_tecnica = models.FileField(upload_to='comercial/fichas/', null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    composicion = models.CharField(max_length=150, blank=True)
    colores_disponibles = models.CharField(max_length=255, blank=True)
    tallas_disponibles = models.CharField(max_length=150, blank=True)
    unidad_venta = models.CharField(max_length=30, default='unidad')

    def __str__(self):
        return self.nombre_comercial

class ListaPrecio(models.Model):
    """Diferentes listas de precios (PVP, Mayorista, Distribuidor, etc.)"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    moneda = models.CharField(
        max_length=3,
        choices=[('VES', 'Bolívares (VES)'), ('USD', 'Dólares (USD)'), ('EUR', 'Euros (EUR)')],
        default='USD',
        verbose_name='Moneda',
    )
    factor_ajuste = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, help_text="Factor multiplicador global (opcional)")

    def __str__(self):
        return f"{self.nombre} ({self.moneda})"

class ItemPrecio(models.Model):
    lista = models.ForeignKey(ListaPrecio, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_maximo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('lista', 'producto')

    def __str__(self):
        return f"{self.producto.nombre} en {self.lista.nombre}"


class OrdenProduccionComercial(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('validacion', 'En validación'),
        ('enviada', 'Enviada a Producción'),
        ('ejecutando', 'En ejecución'),
        ('cerrada', 'Cerrada'),
    ]
    numero = models.CharField(max_length=30, unique=True, blank=True)
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.PROTECT)
    cliente = models.CharField(max_length=200, blank=True)
    fecha = models.DateField()
    fecha_entrega = models.DateField(null=True, blank=True)
    responsable = models.CharField(max_length=150, blank=True)
    descripcion = models.TextField(blank=True)
    genero = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=100, blank=True)
    tipo_tela = models.CharField(max_length=200, blank=True)
    tallas = models.CharField(max_length=200, blank=True)
    cantidades_talla = models.JSONField(default=dict, blank=True)
    cantidad_total = models.PositiveIntegerField(default=0)
    materiales = models.JSONField(default=list, blank=True)
    hoja_consumo = models.TextField(blank=True)
    orden_trabajo = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    tipo_solicitud = models.CharField(max_length=80, default='Producción')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    orden_produccion = models.OneToOneField(
        'produccion.OrdenProduccion', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orden_comercial_origen',
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ordenes_comerciales_produccion',
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-fecha', '-creado_en')
        verbose_name = 'Orden comercial de producción'
        verbose_name_plural = 'Órdenes comerciales de producción'

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f'OPC-{self.fecha:%Y%m%d}-{uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero} - {self.producto.nombre}'


class EncuestaSatisfaccionCliente(models.Model):
    CALIFICACIONES = [('E', 'Excelente'), ('B', 'Bueno'), ('R', 'Regular'), ('M', 'Mejorable'), ('D', 'Deficiente')]
    orden = models.ForeignKey(OrdenProduccionComercial, on_delete=models.SET_NULL, null=True, blank=True, related_name='encuestas_satisfaccion')
    organizacion = models.CharField(max_length=200)
    representante = models.CharField(max_length=150)
    cumplimiento_requerimientos = models.CharField(max_length=1, choices=CALIFICACIONES)
    tiempo_respuesta = models.CharField(max_length=1, choices=CALIFICACIONES)
    calidad_servicio = models.CharField(max_length=1, choices=CALIFICACIONES)
    atencion_personal = models.CharField(max_length=1, choices=CALIFICACIONES)
    producto_servicio = models.CharField(max_length=1, choices=CALIFICACIONES)
    comentarios = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    respondida_por = models.CharField(max_length=150)
    cargo = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    correo = models.EmailField(blank=True)
    fecha = models.DateField()
    registrada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if any(getattr(self, campo) in ('R', 'M', 'D') for campo in (
            'cumplimiento_requerimientos', 'tiempo_respuesta', 'calidad_servicio',
            'atencion_personal', 'producto_servicio',
        )) and not self.comentarios.strip():
            from django.core.exceptions import ValidationError
            raise ValidationError({'comentarios': 'Los comentarios son obligatorios para una calificación regular o inferior.'})


class SolicitudCotizacion(models.Model):
    """Requerimiento comercial recibido y trazable hasta su cotización."""
    TIPOS = [('fabricado', 'Producto fabricado por planta'), ('comercializado', 'Producto no fabricado por planta')]
    ESTADOS = [
        ('recibida', 'Recibida'), ('en_analisis', 'En análisis'),
        ('cotizada', 'Cotizada'), ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'), ('cerrada', 'Cerrada'),
    ]
    numero = models.CharField(max_length=30, unique=True, blank=True)
    cliente = models.CharField(max_length=200)
    contacto = models.CharField(max_length=150, blank=True)
    correo = models.EmailField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='fabricado')
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.PROTECT, null=True, blank=True)
    requerimiento = models.TextField(help_text='Especificaciones técnicas y cantidades solicitadas.')
    fecha_recepcion = models.DateField()
    fecha_limite_cotizacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='recibida')
    responsable = models.CharField(max_length=150, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-fecha_recepcion', '-creado_en')
        verbose_name = 'Solicitud de cotización'
        verbose_name_plural = 'Solicitudes de cotización'

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f'SC-{self.fecha_recepcion:%Y%m%d}-{uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero} - {self.cliente}'


class CotizacionComercial(models.Model):
    ESTADOS = [('borrador', 'Borrador'), ('enviada', 'Enviada'), ('aceptada', 'Aceptada'), ('vencida', 'Vencida'), ('rechazada', 'Rechazada')]
    solicitud = models.OneToOneField(SolicitudCotizacion, on_delete=models.PROTECT, related_name='cotizacion')
    numero = models.CharField(max_length=30, unique=True, blank=True)
    fecha = models.DateField()
    vigencia_hasta = models.DateField()
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    moneda = models.CharField(max_length=3, default='VES')
    condiciones_pago = models.CharField(max_length=250, blank=True)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='borrador')
    aprobada_por_cliente = models.BooleanField(default=False)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-fecha', '-creado_en')

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f'COT-{self.fecha:%Y%m%d}-{uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    @property
    def total(self):
        return self.subtotal + self.impuesto

    def __str__(self):
        return f'{self.numero} - {self.solicitud.cliente}'


class ReclamoComercial(models.Model):
    CANALES = [('digital', 'Digital'), ('escrito', 'Escrito')]
    ESTADOS = [('recibido', 'Recibido'), ('en_investigacion', 'En investigación'), ('respondido', 'Respondido'), ('cerrado', 'Cerrado')]
    numero = models.CharField(max_length=30, unique=True, blank=True)
    cliente = models.CharField(max_length=200)
    orden = models.ForeignKey(OrdenProduccionComercial, on_delete=models.SET_NULL, null=True, blank=True, related_name='reclamos')
    fecha_recepcion = models.DateField()
    canal = models.CharField(max_length=10, choices=CANALES, default='digital')
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    causa = models.TextField(blank=True)
    acciones = models.TextField(blank=True)
    respuesta = models.TextField(blank=True)
    fecha_respuesta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='recibido')
    responsable = models.CharField(max_length=150, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-fecha_recepcion', '-creado_en')

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f'REC-{self.fecha_recepcion:%Y%m%d}-{uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    @property
    def fecha_limite_respuesta(self):
        from datetime import timedelta
        return self.fecha_recepcion + timedelta(days=5)

    def __str__(self):
        return f'{self.numero} - {self.cliente}'


class SolicitudDonacion(models.Model):
    ESTADOS = [('recibida', 'Recibida'), ('en_revision', 'En revisión'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('entregada', 'Entregada')]
    numero = models.CharField(max_length=30, unique=True, blank=True)
    beneficiario = models.CharField(max_length=200)
    institucion_solicitante = models.CharField(max_length=250)
    fecha_solicitud = models.DateField()
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.PROTECT, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    justificacion = models.TextField()
    aprobacion_presidencia = models.BooleanField(default=False)
    contrato_donacion = models.FileField(upload_to='comercial/donaciones/', null=True, blank=True)
    carta_aceptacion = models.FileField(upload_to='comercial/donaciones/', null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='recibida')
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-fecha_solicitud', '-creado_en')
        verbose_name = 'Solicitud de donación'
        verbose_name_plural = 'Solicitudes de donación'

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f'DON-{self.fecha_solicitud:%Y%m%d}-{uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero} - {self.beneficiario}'