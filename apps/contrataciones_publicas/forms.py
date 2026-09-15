from django import forms

from .models import (
    Contrato, EvaluacionContratacion, NormaContratacion, OfertaProveedor,
    ProcesoContratacion, Proveedor,
)


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


def form_for(model, exclude=()):
    return type(f'{model.__name__}Form', (BaseForm,), {
        'Meta': type('Meta', (), {'model': model, 'fields': '__all__', 'exclude': exclude})
    })


ProveedorForm = form_for(Proveedor)
ProcesoContratacionForm = form_for(ProcesoContratacion, ('aprobado_por',))
OfertaProveedorForm = form_for(OfertaProveedor)
EvaluacionContratacionForm = form_for(EvaluacionContratacion)
ContratoForm = form_for(Contrato)
NormaContratacionForm = form_for(NormaContratacion)
