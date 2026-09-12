from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Almacen(models.Model):
    """Representa un lugar físico de almacenamiento (Materias primas, rollos, producto terminado)"""
    TIPOS = [
        ('repuestos', 'Repuestos de máquinas de confección'),
        ('materias_primas', 'Telas e hilos'),
        ('consumibles', 'Consumibles textiles'),
        ('producto_terminado', 'Producto terminado'),
        ('general', 'General'),
    ]
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=30, choices=TIPOS, default='general')
    es_principal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Almacenes"


class RepuestoMaquina(models.Model):
    TIPOS = [
        ('aguja', 'Agujas'),
        ('cuchilla', 'Cuchillas'),
        ('correa', 'Correas'),
        ('motor', 'Motores'),
        ('otro', 'Otro'),
    ]
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='otro')
    maquina_compatible = models.CharField(max_length=150, blank=True)
    unidad_medida = models.CharField(max_length=20, default='unidad')
    stock_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ExistenciaAlmacen(models.Model):
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='existencias')
    materia_prima = models.ForeignKey('produccion.MateriaPrima', on_delete=models.CASCADE, null=True, blank=True)
    producto_pt = models.ForeignKey('produccion.ProductoTerminado', on_delete=models.CASCADE, null=True, blank=True)
    repuesto = models.ForeignKey(RepuestoMaquina, on_delete=models.PROTECT, null=True, blank=True)
    stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('almacen', 'materia_prima'), name='unique_existencia_materia_prima'),
            models.UniqueConstraint(fields=('almacen', 'producto_pt'), name='unique_existencia_producto'),
            models.UniqueConstraint(fields=('almacen', 'repuesto'), name='unique_existencia_repuesto'),
            models.CheckConstraint(
                condition=(
                    models.Q(materia_prima__isnull=False, producto_pt__isnull=True, repuesto__isnull=True)
                    | models.Q(materia_prima__isnull=True, producto_pt__isnull=False, repuesto__isnull=True)
                    | models.Q(materia_prima__isnull=True, producto_pt__isnull=True, repuesto__isnull=False)
                ),
                name='existencia_un_solo_item',
            ),
        ]

    def __str__(self):
        item = (
            self.materia_prima.nombre if self.materia_prima
            else self.producto_pt.nombre if self.producto_pt
            else self.repuesto.nombre if self.repuesto
            else "Desconocido"
        )
        return f"{self.almacen.nombre} - {item}: {self.stock}"

class MovimientoInventario(models.Model):
    """Historial de entradas y salidas de stock para control logístico."""
    TIPO_MOVIMIENTO = [
        ('E', 'Entrada'),
        ('S', 'Salida'),
        ('T', 'Transferencia'),
    ]
    
    MOTIVOS = [
        ('compra', 'Recepción de Compra'),
        ('produccion', 'Producción de Lote / Rollo'),
        ('consumo', 'Consumo en Planta Textil'),
        ('venta', 'Despacho de Venta'),
        ('ajuste', 'Ajuste de Inventario'),
        ('transferencia', 'Transferencia entre Almacenes'),
    ]
    
    materia_prima = models.ForeignKey('produccion.MateriaPrima', on_delete=models.PROTECT, related_name='movimientos', null=True, blank=True)
    producto_pt = models.ForeignKey('produccion.ProductoTerminado', on_delete=models.PROTECT, related_name='movimientos', null=True, blank=True)
    repuesto = models.ForeignKey(RepuestoMaquina, on_delete=models.PROTECT, related_name='movimientos', null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=TIPO_MOVIMIENTO)
    motivo = models.CharField(max_length=20, choices=MOTIVOS, default='ajuste')
    almacen_origen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='salidas', null=True, blank=True)
    almacen_destino = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='entradas', null=True, blank=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_stock = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_logistica')
    referencia = models.CharField(max_length=100, null=True, blank=True, help_text="Ej: Consumo OP-123, Lote Hilo #45")

    def clean(self):
        super().clean()
        items = [self.materia_prima, self.producto_pt, self.repuesto]
        if sum(item is not None for item in items) != 1:
            raise ValidationError('El movimiento debe referir exactamente un artículo.')
        if self.tipo == 'E' and not self.almacen_destino:
            raise ValidationError({'almacen_destino': 'Una entrada requiere almacén destino.'})
        if self.tipo == 'S' and not self.almacen_origen:
            raise ValidationError({'almacen_origen': 'Una salida requiere almacén origen.'})
        if self.tipo == 'T' and (not self.almacen_origen or not self.almacen_destino):
            raise ValidationError('Una transferencia requiere origen y destino.')

    def __str__(self):
        item = (
            self.materia_prima.nombre if self.materia_prima
            else self.producto_pt.nombre if self.producto_pt
            else self.repuesto.nombre if self.repuesto
            else "Desconocido"
        )
        return f"{self.get_tipo_display()} - {item} ({self.cantidad})"
