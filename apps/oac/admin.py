from django.contrib import admin
from .models import BusquedaMedicamento, CitaCiudadana, Donacion, JornadaMedica, PersonalOAC, PresupuestoOAC

admin.site.register([PersonalOAC, PresupuestoOAC, Donacion, CitaCiudadana, BusquedaMedicamento, JornadaMedica])
