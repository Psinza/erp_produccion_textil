from django.contrib import admin

from .models import (
    EquipoServicios, PersonalServicios, PlanMantenimiento, SolicitudMaterial,
    SolicitudServicio, TareaDiaria, Ubicacion,
)


admin.site.register([
    Ubicacion, PersonalServicios, TareaDiaria, PlanMantenimiento,
    EquipoServicios, SolicitudMaterial, SolicitudServicio,
])
