from django import forms

from .models import (
    EquipoServicios, PersonalServicios, PlanMantenimiento, SolicitudMaterial,
    SolicitudServicio, TareaDiaria, Ubicacion,
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


UbicacionForm = make_form(Ubicacion)
PersonalServiciosForm = make_form(PersonalServicios)
TareaDiariaForm = make_form(TareaDiaria)
PlanMantenimientoForm = make_form(PlanMantenimiento)
EquipoServiciosForm = make_form(EquipoServicios)
SolicitudMaterialForm = make_form(SolicitudMaterial)
SolicitudServicioForm = make_form(SolicitudServicio)
