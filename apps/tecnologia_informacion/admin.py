from django.contrib import admin

from .models import (
    AsignacionDiaria, EquipoTI, IndicadorGestion, MantenimientoEquipo,
    MonitoreoRed, PersonalTI, PlanModernizacion, PlanTrabajoTI,
    RecepcionEquipo, ServicioTI, SolicitudEquipo, TicketTI,
)


admin.site.register([
    PersonalTI, TicketTI, MonitoreoRed, AsignacionDiaria, EquipoTI,
    MantenimientoEquipo, PlanTrabajoTI, SolicitudEquipo, RecepcionEquipo,
    IndicadorGestion, ServicioTI, PlanModernizacion,
])
