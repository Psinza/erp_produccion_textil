from django import forms

from .models import BusquedaMedicamento, CitaCiudadana, Donacion, JornadaMedica, PersonalOAC, PresupuestoOAC


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


def make_form(model):
    return type(f'{model.__name__}Form', (BaseForm,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})


PersonalOACForm = make_form(PersonalOAC)
PresupuestoOACForm = make_form(PresupuestoOAC)
DonacionForm = make_form(Donacion)
CitaCiudadanaForm = make_form(CitaCiudadana)
BusquedaMedicamentoForm = make_form(BusquedaMedicamento)
JornadaMedicaForm = make_form(JornadaMedica)
