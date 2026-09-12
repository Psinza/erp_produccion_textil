from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrdenProduccion
from apps.logistica.models import MovimientoInventario, Almacen

@receiver(post_save, sender=OrdenProduccion)
def actualizar_stock_produccion_completada(sender, instance, created, **kwargs):
    """
    Actualiza el stock del ProductoTerminado cuando la OrdenProduccion es 'completada'
    y descuenta las materias primas utilizadas.
    """
    if instance.estado == 'completada':
        referencia_lote = f"Producción Lote: {instance.lote_numero}"
        
        # Evitar duplicados
        if not MovimientoInventario.objects.filter(referencia=referencia_lote).exists():
            
            # Buscar almacén principal (o el primero que exista)
            almacen_defecto = Almacen.objects.filter(es_principal=True).first() or Almacen.objects.first()
            
            if not almacen_defecto:
                print("Advertencia: No hay almacenes configurados para procesar la producción.")
                return

            # 1. Entrada de Producto Terminado
            MovimientoInventario.objects.create(
                producto_pt=instance.producto,
                tipo='E', # Entrada
                motivo='produccion',
                almacen_destino=almacen_defecto,
                cantidad=instance.piezas_producidas_ok,
                referencia=referencia_lote,
            )