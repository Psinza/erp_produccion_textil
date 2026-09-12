from django.conf import settings
from django.db import models
from decimal import Decimal
from django.utils import timezone
from apps.facturacion.models import Proveedor
# Asumiendo que existe un modelo Producto en apps.inventarios o logistica, o usaremos un string por ahora
# from apps.inventarios.models import Producto

class ProductoCompra(models.Model):
    MONEDAS = [('VES', 'Bolívares (VES)'), ('USD', 'Dólares (USD)'), ('EUR', 'Euros (EUR)')]
    TIPOS = [
        ('tela', 'Tela'),
        ('hilo', 'Hilo'),
        ('consumible', 'Consumible textil'),
        ('repuesto', 'Repuesto de máquina'),
        ('servicio', 'Servicio'),
    ]
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    precio_referencia = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    moneda = models.CharField(max_length=3, choices=MONEDAS, default='USD', verbose_name='Moneda')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='consumible')
    unidad_medida = models.CharField(max_length=20, default='unidad')
    especificacion_textil = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    MONEDAS = [('VES', 'Bolívares (VES)'), ('USD', 'Dólares (USD)'), ('EUR', 'Euros (EUR)')]
    numero = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    moneda = models.CharField(max_length=3, choices=MONEDAS, default='USD', verbose_name='Moneda')
    fecha_emision = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=[('borrador', 'Borrador'), ('aprobada', 'Aprobada'), ('recibida', 'Recibida')], default='borrador')
    total = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    requerimiento = models.ForeignKey(
        'RequerimientoMaterial', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ordenes_compra'
    )

    def cantidad_recibida(self, detalle):
        return detalle.recepciones.aggregate(total=models.Sum('cantidad'))['total'] or 0

    def __str__(self):
        return f"OC-{self.numero}"


class RequerimientoMaterial(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('atendido', 'Atendido'),
        ('anulado', 'Anulado'),
    ]
    numero = models.CharField(max_length=30, unique=True)
    orden_produccion = models.ForeignKey(
        'produccion.OrdenProduccion', on_delete=models.PROTECT,
        related_name='requerimientos_compra', null=True, blank=True
    )
    solicitud_pieza = models.ForeignKey(
        'produccion.SolicitudPiezaMecanica', on_delete=models.PROTECT,
        related_name='requerimientos_compra', null=True, blank=True,
    )
    almacen_destino = models.ForeignKey(
        'logistica.Almacen', on_delete=models.PROTECT,
        related_name='requerimientos_compra', null=True, blank=True,
        limit_choices_to={'tipo': 'repuestos', 'activo': True},
    )
    solicitado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    fecha_requerida = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        origen = (
            f'pieza {self.solicitud_pieza.pk}'
            if self.solicitud_pieza_id
            else f'lote {self.orden_produccion.lote_numero}'
            if self.orden_produccion_id
            else 'sin origen'
        )
        return f'{self.numero} - {origen}'


class DetalleRequerimientoMaterial(models.Model):
    requerimiento = models.ForeignKey(RequerimientoMaterial, on_delete=models.CASCADE, related_name='detalles')
    materia_prima = models.ForeignKey('produccion.MateriaPrima', on_delete=models.PROTECT, null=True, blank=True)
    repuesto = models.ForeignKey('logistica.RepuestoMaquina', on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    especificacion = models.TextField(blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if bool(self.materia_prima) == bool(self.repuesto):
            raise ValidationError('Cada detalle debe referir una materia prima o un repuesto.')


class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    materia_prima = models.ForeignKey('produccion.MateriaPrima', on_delete=models.PROTECT, null=True, blank=True)
    repuesto = models.ForeignKey('logistica.RepuestoMaquina', on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    moneda = models.CharField(max_length=3, choices=OrdenCompra.MONEDAS, default='USD', verbose_name='Moneda')

    def clean(self):
        from django.core.exceptions import ValidationError
        if bool(self.materia_prima) == bool(self.repuesto):
            raise ValidationError('El detalle debe referir materia prima o repuesto.')


class RecepcionCompra(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('parcial', 'Parcial'), ('completa', 'Completa'), ('anulada', 'Anulada')]
    orden = models.ForeignKey(OrdenCompra, on_delete=models.PROTECT, related_name='recepciones')
    almacen = models.ForeignKey('logistica.Almacen', on_delete=models.PROTECT, related_name='recepciones_compra')
    factura = models.ForeignKey('FacturaCompra', on_delete=models.SET_NULL, null=True, blank=True, related_name='recepciones')
    numero_acta = models.CharField(max_length=40, unique=True)
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    recibido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True)


class DetalleRecepcionCompra(models.Model):
    recepcion = models.ForeignKey(RecepcionCompra, on_delete=models.CASCADE, related_name='detalles')
    detalle_orden = models.ForeignKey(DetalleOrdenCompra, on_delete=models.PROTECT, related_name='recepciones')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    aceptado = models.BooleanField(default=True)

class FacturaCompra(models.Model):
    MONEDAS = [('VES', 'Bolívares (VES)'), ('USD', 'Dólares (USD)'), ('EUR', 'Euros (EUR)')]
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='facturas_compra')
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')
    moneda = models.CharField(max_length=3, choices=MONEDAS, default='USD', verbose_name='Moneda')
    almacen_recepcion = models.ForeignKey(
        'logistica.Almacen', on_delete=models.PROTECT, null=True, blank=True,
        related_name='facturas_compra_recibidas',
    )
    
    numero_factura = models.CharField(max_length=50)
    numero_control = models.CharField(max_length=50, help_text="Número de control fiscal")
    fecha_emision = models.DateField()
    fecha_recepcion = models.DateField(default=timezone.now)
    
    # Desglose de impuestos
    exento = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    base_imponible = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    base_imponible_reducida = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    base_imponible_suntuaria = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    
    monto_iva_general = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    monto_iva_reducida = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    monto_iva_suntuaria = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    
    igtf = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    
    total = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    
    estado = models.CharField(max_length=20, choices=[('registrada', 'Registrada'), ('pagada', 'Pagada'), ('anulada', 'Anulada')], default='registrada')
    registrada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Factura de Compra"
        verbose_name_plural = "Facturas de Compra"
        unique_together = ('proveedor', 'numero_factura')

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.proveedor.razon_social}"

class DetalleFacturaCompra(models.Model):
    factura = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, related_name='detalles')
    materia_prima = models.ForeignKey(
        'produccion.MateriaPrima', on_delete=models.PROTECT, null=True, blank=True,
        related_name='detalles_facturas_compra',
    )
    repuesto = models.ForeignKey(
        'logistica.RepuestoMaquina', on_delete=models.PROTECT, null=True, blank=True,
        related_name='detalles_facturas_compra',
    )
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    tipo_impuesto = models.CharField(max_length=20, choices=[('exento', 'Exento'), ('general', 'General (16%)'), ('reducida', 'Reducida (8%)'), ('suntuaria', 'Suntuaria (31%)')], default='general')
    monto_impuesto = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)

    def clean(self):
        from django.core.exceptions import ValidationError
        if bool(self.materia_prima) == bool(self.repuesto):
            raise ValidationError('El detalle debe referir una materia prima o un repuesto.')
        if self.cantidad <= 0:
            raise ValidationError({'cantidad': 'La cantidad recibida debe ser mayor que cero.'})

    def save(self, *args, **kwargs):
        base = self.cantidad * self.precio_unitario
        if self.tipo_impuesto == 'general':
            self.monto_impuesto = base * Decimal('0.16')
        elif self.tipo_impuesto == 'reducida':
            self.monto_impuesto = base * Decimal('0.08')
        elif self.tipo_impuesto == 'suntuaria':
            self.monto_impuesto = base * Decimal('0.31')
        else:
            self.monto_impuesto = Decimal('0.00')
            
        self.subtotal = base + self.monto_impuesto
        super().save(*args, **kwargs)
