from django.conf import settings
from django.db import models
from decimal import Decimal

class CategoriaMateriaPrima(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías de Materias Primas"

class MateriaPrima(models.Model):
    UNIDADES = [
        ('kg', 'Kilogramos'),
        ('m', 'Metros lineales'),
        ('cono', 'Conos de hilo'),
        ('lts', 'Litros (Tintes/Químicos)'),
    ]
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(CategoriaMateriaPrima, on_delete=models.PROTECT, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES, default='kg')
    stock_actual = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"

class CategoriaProductoTerminado(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías de Productos Terminados"

class ProductoTerminado(models.Model):
    TIPO_PRENDA = [
        ('deportivo', 'Uniforme Deportivo'),
        ('militar_gala', 'Uniforme Militar de Gala'),
        ('militar_tropa', 'Uniforme Militar de Tropa'),
        ('institucional', 'Ropa Institucional'),
        ('otro', 'Otro'),
    ]
    nombre = models.CharField(max_length=200)
    tipo_prenda = models.CharField(max_length=30, choices=TIPO_PRENDA, default='institucional')
    categoria = models.ForeignKey(CategoriaProductoTerminado, on_delete=models.PROTECT, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    gramaje = models.DecimalField(max_digits=6, decimal_places=2, help_text="g/m2", null=True, blank=True)
    ancho = models.DecimalField(max_digits=6, decimal_places=2, help_text="Ancho en cm", null=True, blank=True)
    stock_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    costo_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_prenda_display()})"

class OrdenProduccion(models.Model):
    ESTADOS = [
        ('planificada', 'Planificada (UDP)'),
        ('en_corte', 'En Corte'),
        ('en_bordado', 'En Bordados'),
        ('en_produccion', 'En Confección / Producción'),
        ('en_despacho', 'En Despacho / Empaque'),
        ('en_calidad', 'Control de Calidad ISO 9001'),
        ('completada', 'Completada y Notificada'),
        ('anulada', 'Anulada'),
    ]
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    lote_numero = models.CharField(max_length=50, unique=True, verbose_name="Lote / Orden ID")
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.PROTECT)
    cantidad_a_producir = models.PositiveIntegerField(default=1, help_text="Cantidad de piezas requeridas")
    estado = models.CharField(max_length=25, choices=ESTADOS, default='planificada')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media')
    fecha_planificada = models.DateField(null=True, blank=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    piezas_realizadas = models.PositiveIntegerField(default=0)
    piezas_producidas_ok = models.PositiveIntegerField(default=0)
    piezas_rechazadas = models.PositiveIntegerField(default=0)
    
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Lote {self.lote_numero} - {self.producto.nombre} [{self.get_estado_display()}]"

# --- DEPARTAMENTOS ACTUALIZADOS ---

class DepartamentoUDP(models.Model):
    TIPO_UNIFORME_CHOICES = [
        ('militar', 'Uniformes Militares (Camisolas, Chaquetas, Gorras)'),
        ('corporativo', 'Uniformes Corporativos (Camisas, Pantalones, Blazers)'),
        ('deportivo', 'Uniformes Deportivos (Jerseys, Shorts, Chándales)'),
        ('escolar', 'Uniformes Escolares (Pantalones, Polos, Suéteres)'),
    ]
    
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, null=True, blank=True, related_name='udp_list')
    proyecto = models.CharField(max_length=150, null=True, blank=True)
    tipo_uniforme = models.CharField(max_length=30, choices=TIPO_UNIFORME_CHOICES, default='corporativo')
    tipo_diseno = models.CharField(max_length=150, null=True, blank=True, help_text="Ej: Camisolas Ripstop, Polo Piqué, Jersey Dry-Fit")
    cantidad_disenos = models.PositiveIntegerField(default=0)
    piezas_por_diseno = models.PositiveIntegerField(default=0)
    
    rango_tallas = models.CharField(max_length=100, blank=True, null=True, help_text="Ej: XS a 3XL, 14.5/32 a 18/36, o Tallas 4 a 16")
    tipo_tela = models.CharField(max_length=200, blank=True, null=True, help_text="Ej: Ripstop 65/35, Popelina, Oxford, Piqué 50/50")
    especificaciones_tecnicas = models.TextField(blank=True, null=True, help_text="Detalles de gramaje, acabados repelentes, tramado air-mesh, etc.")
    
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"UDP: {self.proyecto or 'Sin proyecto'} - {self.get_tipo_uniforme_display()}"

class DepartamentoCorte(models.Model):
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, null=True, blank=True, related_name='corte_list')
    tela_tendida_metros = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    disenos_recibidos = models.PositiveIntegerField(default=0)
    piezas_por_lote = models.PositiveIntegerField(default=0)
    piezas_defectuosas_corte = models.PositiveIntegerField(default=0)
    fecha_corte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Corte - Lote: {self.orden.lote_numero if self.orden else 'Sin Orden'}"

class DepartamentoProduccionTextil(models.Model):
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, null=True, blank=True, related_name='produccion_textil_list')
    linea_produccion = models.CharField(max_length=100, blank=True, null=True)
    productos_realizados = models.PositiveIntegerField(default=0)
    piezas_con_falla_costura = models.PositiveIntegerField(default=0)
    fecha_produccion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Línea {self.linea_produccion} - {self.productos_realizados} uds"

class DepartamentoBordado(models.Model):
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='bordados')
    operario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion_bordado = models.CharField(max_length=200, help_text="Ej: Escudo Militar, Logo Institucional, Nombre")
    piezas_bordadas_ok = models.PositiveIntegerField(default=0)
    piezas_rechazadas_bordado = models.PositiveIntegerField(default=0)
    fecha_proceso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bordado - Lote {self.orden.lote_numero}: {self.descripcion_bordado}"

class DepartamentoDespacho(models.Model):
    orden = models.OneToOneField(OrdenProduccion, on_delete=models.CASCADE, related_name='despacho')
    responsable_empaque = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    planchado_ok = models.BooleanField(default=False)
    empaquetado_ok = models.BooleanField(default=False)
    piezas_empaquetadas = models.PositiveIntegerField(default=0)
    fecha_empaque = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Despacho/Empaque - Lote {self.orden.lote_numero}"

class DepartamentoCalidadISO9001(models.Model):
    orden = models.OneToOneField(OrdenProduccion, on_delete=models.CASCADE, related_name='calidad_iso')
    auditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    cumple_iso_9001 = models.BooleanField(default=False, help_text="Certifica cumplimiento de normas ISO 9001")
    gramaje_verificado = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    piezas_aprobadas_qc = models.PositiveIntegerField(default=0)
    piezas_rechazadas_qc = models.PositiveIntegerField(default=0)
    informe_auditoria = models.TextField(help_text="Detalles del dictamen de calidad y observaciones directivas")
    fecha_auditoria = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado_qc = "APROBADO ISO 9001" if self.cumple_iso_9001 else "RECHAZADO"
        return f"Calidad QC - Lote {self.orden.lote_numero} [{estado_qc}]"

DepartamentoProduccion = DepartamentoProduccionTextil