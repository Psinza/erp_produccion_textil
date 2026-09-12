from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.logistica.models import Almacen, MovimientoInventario
from .models import (
    CatalogoProceso,
    IndicadorProceso,
    NoConformidad,
    OrdenProduccion,
    ProductoTerminado,
)


class ProduccionTextilTestCase(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username='supervisor-produccion',
            password='test-password',
        )
        self.producto = ProductoTerminado.objects.create(
            nombre='Camisa de prueba',
            sku='TEST-CAMISA-001',
        )

    def test_catalogo_inicial_contiene_seis_procesos_y_kpi(self):
        self.assertEqual(CatalogoProceso.objects.count(), 6)
        self.assertEqual(IndicadorProceso.objects.count(), 6)
        self.assertTrue(IndicadorProceso.objects.filter(codigo='FPY-POOL').exists())

    def test_no_conformidad_conserva_trazabilidad_del_lote(self):
        orden = OrdenProduccion.objects.create(
            lote_numero='TEST-NC-001',
            producto=self.producto,
            cantidad_a_producir=100,
            responsable=self.usuario,
        )
        no_conformidad = NoConformidad.objects.create(
            orden=orden,
            origen='pool',
            descripcion='Falla de costura detectada en inspección final.',
            cantidad_afectada=8,
            porcentaje_rechazo=Decimal('8.00'),
            responsable=self.usuario,
        )
        self.assertEqual(no_conformidad.orden_id, orden.id)
        self.assertEqual(no_conformidad.get_estado_display(), 'Abierta')

    def test_completar_orden_registra_producto_terminado_en_almacen(self):
        almacen = Almacen.objects.create(nombre='Almacén de producto terminado', es_principal=True)
        orden = OrdenProduccion.objects.create(
            lote_numero='TEST-INV-001',
            producto=self.producto,
            cantidad_a_producir=20,
            piezas_producidas_ok=18,
            responsable=self.usuario,
        )
        orden.estado = 'completada'
        orden.save()
        movimiento = MovimientoInventario.objects.get(referencia='Producción Lote: TEST-INV-001')
        self.assertEqual(movimiento.producto_pt_id, self.producto.id)
        self.assertEqual(movimiento.cantidad, Decimal('18'))
        self.assertEqual(movimiento.almacen_destino_id, almacen.id)
