from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CategoriaMateriaPrima(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías de Materias Primas"

class MateriaPrima(models.Model):
    TIPOS_INSUMO = [
        ('tela', 'Tela'),
        ('hilo', 'Hilo'),
        ('boton', 'Botones'),
        ('cremallera', 'Cremalleras'),
        ('goma', 'Gomas'),
        ('cinta', 'Cintas'),
        ('otro', 'Otro consumible'),
    ]
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
    tipo_insumo = models.CharField(max_length=20, choices=TIPOS_INSUMO, default='otro')
    especificacion_tecnica = models.CharField(max_length=255, blank=True)
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


class FichaTecnica(models.Model):
    producto = models.OneToOneField(
        ProductoTerminado, on_delete=models.CASCADE, related_name='ficha_tecnica_produccion'
    )
    version = models.CharField(max_length=20, default='1.0')
    descripcion = models.TextField(blank=True)
    metraje_tela_por_unidad = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    consumo_hilo_por_unidad = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    unidad_consumo_hilo = models.CharField(max_length=10, default='m')
    tolerancia_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    aprobada = models.BooleanField(default=False)
    actualizada_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ficha {self.producto.nombre} v{self.version}'

    def calcular_consumo(self, cantidad):
        factor = 1 + (self.tolerancia_porcentaje / 100)
        return {
            'tela': self.metraje_tela_por_unidad * cantidad * factor,
            'hilo': self.consumo_hilo_por_unidad * cantidad * factor,
        }


class MaterialFichaTecnica(models.Model):
    ficha = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE, related_name='materiales')
    materia_prima = models.ForeignKey('MateriaPrima', on_delete=models.PROTECT)
    cantidad_por_unidad = models.DecimalField(max_digits=10, decimal_places=4)
    desperdicio_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    observaciones = models.CharField(max_length=255, blank=True)

    def cantidad_requerida(self, unidades):
        factor = 1 + (self.desperdicio_porcentaje / 100)
        return self.cantidad_por_unidad * unidades * factor

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
    pedido_origen = models.ForeignKey(
        'ventas.Pedido', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ordenes_produccion',
    )

    def __str__(self):
        return f"Lote {self.lote_numero} - {self.producto.nombre} [{self.get_estado_display()}]"


class LineaProduccion(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    codigo = models.CharField(max_length=30, unique=True)
    activa = models.BooleanField(default=True)
    capacidad_diaria = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class MaquinaTextil(models.Model):
    ESTADOS = [
        ('operativa', 'Operativa'),
        ('mantenimiento', 'En mantenimiento'),
        ('fuera_servicio', 'Fuera de servicio'),
    ]
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=100, help_text='Ej. overlock, recta, cortadora, bordadora')
    marca = models.CharField(max_length=80, blank=True)
    modelo = models.CharField(max_length=80, blank=True)
    serial = models.CharField(max_length=100, blank=True)
    linea = models.ForeignKey(LineaProduccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='maquinas')
    ubicacion = models.CharField(max_length=120, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='operativa')
    horas_operacion = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class SolicitudPiezaMecanica(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('atendida', 'Atendida'), ('anulada', 'Anulada')]
    maquina = models.ForeignKey(MaquinaTextil, on_delete=models.PROTECT, related_name='solicitudes_piezas')
    pieza = models.ForeignKey('logistica.RepuestoMaquina', on_delete=models.PROTECT, null=True, blank=True, related_name='solicitudes_mecanica')
    pieza_nueva = models.CharField(max_length=200, blank=True, verbose_name='Nombre de pieza nueva')
    especificacion_pieza = models.TextField(blank=True, verbose_name='Especificación de la pieza')
    cantidad = models.PositiveIntegerField(default=1)
    prioridad = models.CharField(max_length=20, choices=[('normal', 'Normal'), ('urgente', 'Urgente')], default='normal')
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.pieza and not self.pieza_nueva.strip():
            raise ValidationError({'pieza_nueva': 'Seleccione un repuesto existente o indique el nombre de la pieza nueva.'})
        if self.pieza and self.pieza_nueva.strip():
            raise ValidationError({'pieza_nueva': 'Use una sola opción: repuesto existente o pieza nueva.'})


class OrdenMantenimientoTextil(models.Model):
    TIPOS = [('preventivo', 'Preventivo'), ('correctivo', 'Correctivo'), ('predictivo', 'Predictivo')]
    ESTADOS = [('planificada', 'Planificada'), ('en_proceso', 'En proceso'), ('completada', 'Completada'), ('cancelada', 'Cancelada')]
    maquina = models.ForeignKey(MaquinaTextil, on_delete=models.PROTECT, related_name='ordenes_mantenimiento')
    tipo = models.CharField(max_length=20, choices=TIPOS, default='preventivo')
    descripcion = models.TextField()
    fecha_programada = models.DateField()
    fecha_cierre = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='planificada')
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    costo_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)


class ChequeoLineaProduccion(models.Model):
    linea = models.ForeignKey(LineaProduccion, on_delete=models.PROTECT, related_name='chequeos')
    fecha = models.DateField()
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    maquinas_operativas = models.PositiveIntegerField(default=0)
    maquinas_con_falla = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(blank=True)
    liberada = models.BooleanField(default=False)


class PlanMantenimientoTextil(models.Model):
    nombre = models.CharField(max_length=150)
    linea = models.ForeignKey(LineaProduccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='planes_mantenimiento')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    frecuencia_dias = models.PositiveIntegerField(default=30)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

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
    requerimiento_materiales = models.TextField(blank=True, help_text="Materiales, cantidades y tolerancias requeridas.")
    ficha_tecnica = models.TextField(blank=True, help_text="Ficha técnica aprobada de la prenda.")
    aprobado = models.BooleanField(default=False)
    
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"UDP: {self.proyecto or 'Sin proyecto'} - {self.get_tipo_uniforme_display()}"

class DepartamentoCorte(models.Model):
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, null=True, blank=True, related_name='corte_list')
    tela_tendida_metros = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    disenos_recibidos = models.PositiveIntegerField(default=0)
    piezas_por_lote = models.PositiveIntegerField(default=0)
    piezas_defectuosas_corte = models.PositiveIntegerField(default=0)
    tipo_tela_validado = models.BooleanField(default=False)
    observaciones_calidad_tela = models.TextField(blank=True)
    corte_habilitado = models.BooleanField(default=False)
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
    fibras_hilos_sueltos_ok = models.BooleanField(default=False)
    observaciones_revision = models.TextField(blank=True)
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


class CatalogoProceso(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    objetivo = models.CharField(max_length=255)
    clausula_iso = models.CharField(max_length=50, default='8.5')
    norma_venezolana = models.CharField(max_length=150, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('codigo',)
        verbose_name = 'Catálogo de proceso'
        verbose_name_plural = 'Catálogo de procesos'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class ProcesoDepartamento(models.Model):
    """Plan documentado del proceso por departamento y orden de producción."""

    DEPARTAMENTOS = [
        ('udp', 'UDP / Diseño'),
        ('corte', 'Corte'),
        ('produccion_textil', 'Producción textil'),
        ('pool', 'Pool de calidad'),
        ('bordados', 'Bordados'),
        ('despacho', 'Despacho'),
    ]
    orden = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        related_name='planes_proceso',
    )
    departamento = models.CharField(max_length=30, choices=DEPARTAMENTOS)
    objetivo = models.CharField(max_length=255)
    entradas = models.TextField()
    actividades = models.TextField()
    salidas = models.TextField()
    responsable = models.CharField(max_length=150)
    criterios_aceptacion = models.TextField()
    clausula_iso = models.CharField(max_length=50, default='8.5')
    norma_venezolana = models.CharField(max_length=150, blank=True)
    version = models.PositiveIntegerField(default=1)
    aprobado = models.BooleanField(default=False)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('orden', 'departamento')
        constraints = [
            models.UniqueConstraint(
                fields=('orden', 'departamento', 'version'),
                name='unique_plan_proceso_version',
            ),
        ]

    def __str__(self):
        return f'{self.orden.lote_numero} - {self.get_departamento_display()} v{self.version}'


class IndicadorProceso(models.Model):
    """Definición de un indicador medible para el proceso textil."""

    TIPO = [('porcentaje', 'Porcentaje'), ('cantidad', 'Cantidad'), ('tiempo', 'Tiempo')]
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=40, unique=True)
    departamento = models.CharField(max_length=30, choices=ProcesoDepartamento.DEPARTAMENTOS)
    objetivo = models.DecimalField(max_digits=12, decimal_places=4)
    unidad = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TIPO, default='porcentaje')
    sentido = models.CharField(max_length=10, choices=[('mayor', 'Mayor es mejor'), ('menor', 'Menor es mejor')], default='mayor')
    clausula_iso = models.CharField(max_length=50, default='9.1')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class MedicionIndicador(models.Model):
    indicador = models.ForeignKey(IndicadorProceso, on_delete=models.CASCADE, related_name='mediciones')
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='mediciones_indicadores')
    valor = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    periodo = models.DateField()
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-periodo', '-creado_en')


class Notificacion(models.Model):
    TIPOS = [('flujo', 'Cambio de flujo'), ('calidad', 'Alerta de calidad'), ('vencimiento', 'Vencimiento')]
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='notificaciones')
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones_produccion')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('leida', '-creada_en')


class NoConformidad(models.Model):
    ESTADOS = [('abierta', 'Abierta'), ('analisis', 'En análisis'), ('cerrada', 'Cerrada')]
    ORIGENES = [('corte', 'Corte'), ('produccion_textil', 'Producción textil'), ('pool', 'Pool'), ('bordados', 'Bordados'), ('despacho', 'Despacho')]
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='no_conformidades')
    origen = models.CharField(max_length=30, choices=ORIGENES)
    descripcion = models.TextField()
    cantidad_afectada = models.PositiveIntegerField(default=1)
    porcentaje_rechazo = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    accion_inmediata = models.TextField(blank=True)
    causa_raiz = models.TextField(blank=True)
    accion_correctiva = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='abierta')
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    cerrada_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-creada_en',)