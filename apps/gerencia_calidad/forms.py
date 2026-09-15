from django import forms
from .models import AuditoriaCalidadISO, IndicadorCalidad, NoConformidad, NormaCalidad, ProcesoCalidad

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

def make_form(model):
    return type(f'{model.__name__}Form', (BaseForm,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})

NormaCalidadForm = make_form(NormaCalidad)
ProcesoCalidadForm = make_form(ProcesoCalidad)
AuditoriaCalidadISOForm = make_form(AuditoriaCalidadISO)
NoConformidadForm = make_form(NoConformidad)
IndicadorCalidadForm = make_form(IndicadorCalidad)
