from django import forms

from .models import (
    AsignacionDiaria, EquipoTI, IndicadorGestion, MantenimientoEquipo,
    MonitoreoRed, PersonalTI, PlanModernizacion, PlanTrabajoTI,
    RecepcionEquipo, ServicioTI, SolicitudEquipo, TicketTI,
)


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


def make_form(model):
    return type(f'{model.__name__}Form', (BaseForm,), {
        'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})
    })


PersonalTIForm = make_form(PersonalTI)
TicketTIForm = make_form(TicketTI)
MonitoreoRedForm = make_form(MonitoreoRed)
AsignacionDiariaForm = make_form(AsignacionDiaria)
EquipoTIForm = make_form(EquipoTI)
MantenimientoEquipoForm = make_form(MantenimientoEquipo)
PlanTrabajoTIForm = make_form(PlanTrabajoTI)
SolicitudEquipoForm = make_form(SolicitudEquipo)
RecepcionEquipoForm = make_form(RecepcionEquipo)
IndicadorGestionForm = make_form(IndicadorGestion)
ServicioTIForm = make_form(ServicioTI)
PlanModernizacionForm = make_form(PlanModernizacion)
