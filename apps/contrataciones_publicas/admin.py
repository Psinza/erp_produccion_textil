from django.contrib import admin

from .models import (
    Contrato, EvaluacionContratacion, NormaContratacion, OfertaProveedor,
    ProcesoContratacion, Proveedor,
)


admin.site.register([
    Proveedor, ProcesoContratacion, OfertaProveedor, EvaluacionContratacion,
    Contrato, NormaContratacion,
])
