from django.contrib import admin
from .models import AccionCorrectiva, HallazgoAuditoria, NormaAuditoria, PlanAuditoria

admin.site.register([PlanAuditoria, HallazgoAuditoria, AccionCorrectiva, NormaAuditoria])
