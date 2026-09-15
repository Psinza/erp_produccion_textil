from django.contrib import admin
from .models import CasoJuridico, ContratoJuridico, DictamenJuridico, NormaLegal
admin.site.register([CasoJuridico, DictamenJuridico, NormaLegal, ContratoJuridico])
