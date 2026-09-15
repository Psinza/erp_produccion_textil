from django.contrib import admin

from .models import (
    DotacionEquipo, EquipoSeguridad, Guardia, IncidenteSeguridad,
    InspeccionSST, MaterialSalida, NormaReferencia, OrdenSalidaMaterial,
    PaseIngreso, PuestoSeguridad, RegistroAcceso, RondaSeguridad,
    TurnoGuardia,
)


admin.site.register([
    PuestoSeguridad, Guardia, TurnoGuardia, EquipoSeguridad, DotacionEquipo,
    PaseIngreso, RegistroAcceso, OrdenSalidaMaterial, MaterialSalida,
    RondaSeguridad, IncidenteSeguridad, InspeccionSST, NormaReferencia,
])
