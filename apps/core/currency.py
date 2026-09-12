from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import TasaBCV


def obtener_tasa_bcv(fecha=None):
    """Obtiene la tasa oficial registrada para la fecha o la última anterior."""
    fecha = fecha or timezone.localdate()
    tasa = TasaBCV.objects.filter(fecha__lte=fecha).order_by('-fecha').first()
    if not tasa:
        raise ValidationError(
            f'No existe una tasa BCV registrada para {fecha:%d/%m/%Y}.'
        )
    return tasa


def convertir_a_ves(monto, codigo_moneda='VES', fecha=None):
    monto = Decimal(monto)
    return obtener_tasa_bcv(fecha).convertir_a_ves(monto, codigo_moneda)
