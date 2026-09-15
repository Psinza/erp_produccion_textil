from django.contrib import admin

from .models import (
    EjercicioPresupuestario, ModificacionPresupuestaria, NormaPresupuesto,
    ObjetivoInstitucional, PartidaPresupuestaria, PlanEstrategico,
    UnidadPresupuestaria,
)


admin.site.register([
    PlanEstrategico, ObjetivoInstitucional, EjercicioPresupuestario,
    UnidadPresupuestaria, PartidaPresupuestaria, ModificacionPresupuestaria,
    NormaPresupuesto,
])
