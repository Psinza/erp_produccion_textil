from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.facturacion.models import Proveedor
from apps.logistica.models import Almacen, MovimientoInventario
from apps.produccion.models import MateriaPrima
from .models import DetalleFacturaCompra, FacturaCompra


class RecepcionFacturaCompraTestCase(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username='compras-test',
            password='test-password',
        )
        self.proveedor = Proveedor.objects.create(
            razon_social='Proveedor Textil C.A.',
            rif='J-12345678-9',
            direccion='Av. Principal',
        )
        self.tela = MateriaPrima.objects.create(
            nombre='Tela de prueba',
            sku='TELA-TEST-001',
            tipo_insumo='tela',
            unidad_medida='m',
        )
        Almacen.objects.create(
            nombre='Recepción telas test', tipo='materias_primas', activo=True
        )

    def test_detalle_de_factura_genera_entrada_en_almacen_textil(self):
        factura = FacturaCompra.objects.create(
            proveedor=self.proveedor,
            numero_factura='FAC-TEST-001',
            numero_control='00-TEST-001',
            fecha_emision=date.today(),
            registrada_por=self.usuario,
        )
        detalle = DetalleFacturaCompra.objects.create(
            factura=factura,
            materia_prima=self.tela,
            descripcion='Tela recibida',
            cantidad=Decimal('125.50'),
            precio_unitario=Decimal('4.00'),
            subtotal=Decimal('502.00'),
        )

        movimiento = MovimientoInventario.objects.get(
            referencia=f'Recepción factura FAC-TEST-001 detalle {detalle.pk}'
        )
        self.assertEqual(movimiento.almacen_destino.tipo, 'materias_primas')
        self.assertEqual(movimiento.cantidad, Decimal('125.50'))
        self.assertEqual(MovimientoInventario.objects.count(), 1)

        detalle.save()
        self.assertEqual(MovimientoInventario.objects.count(), 1)
