from django import forms

from .models import (
    EjercicioPresupuestario, ModificacionPresupuestaria, NormaPresupuesto,
    ObjetivoInstitucional, PartidaPresupuestaria, PlanEstrategico,
    UnidadPresupuestaria,
)


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


def form_for(model, exclude=()):
    return type(f'{model.__name__}Form', (BaseForm,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__', 'exclude': exclude})})


PlanEstrategicoForm = form_for(PlanEstrategico)
ObjetivoInstitucionalForm = form_for(ObjetivoInstitucional)
EjercicioPresupuestarioForm = form_for(EjercicioPresupuestario)
UnidadPresupuestariaForm = form_for(UnidadPresupuestaria)
PartidaPresupuestariaForm = form_for(PartidaPresupuestaria)
ModificacionPresupuestariaForm = form_for(ModificacionPresupuestaria, ('aprobado_por',))
NormaPresupuestoForm = form_for(NormaPresupuesto)
