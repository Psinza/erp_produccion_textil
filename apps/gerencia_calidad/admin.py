from django.contrib import admin
from .models import AuditoriaCalidadISO, IndicadorCalidad, NoConformidad, NormaCalidad, ProcesoCalidad
admin.site.register([NormaCalidad, ProcesoCalidad, AuditoriaCalidadISO, NoConformidad, IndicadorCalidad])
