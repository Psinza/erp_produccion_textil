from django import forms
from .models import AfectacionPersonal, EquipoMedico, PersonalMedico, PresupuestoMedico, ReposoMedico, ResultadoIngreso

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

def make_form(model):
    return type(f'{model.__name__}Form', (BaseForm,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})

PersonalMedicoForm = make_form(PersonalMedico)
PresupuestoMedicoForm = make_form(PresupuestoMedico)
ResultadoIngresoForm = make_form(ResultadoIngreso)
ReposoMedicoForm = make_form(ReposoMedico)
AfectacionPersonalForm = make_form(AfectacionPersonal)
EquipoMedicoForm = make_form(EquipoMedico)
