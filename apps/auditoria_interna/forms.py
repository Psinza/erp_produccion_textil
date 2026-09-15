from django import forms
from .models import AccionCorrectiva, HallazgoAuditoria, NormaAuditoria, PlanAuditoria


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


def make_form(model):
    return type(f'{model.__name__}Form', (BaseForm,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})


PlanAuditoriaForm = make_form(PlanAuditoria)
HallazgoAuditoriaForm = make_form(HallazgoAuditoria)
AccionCorrectivaForm = make_form(AccionCorrectiva)
NormaAuditoriaForm = make_form(NormaAuditoria)
