from django.contrib import admin
from .models import AfectacionPersonal, EquipoMedico, PersonalMedico, PresupuestoMedico, ReposoMedico, ResultadoIngreso

admin.site.register([PersonalMedico, PresupuestoMedico, ResultadoIngreso, ReposoMedico, AfectacionPersonal, EquipoMedico])
