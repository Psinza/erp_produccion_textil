from django import forms
from .models import CasoJuridico, ContratoJuridico, DictamenJuridico, NormaLegal

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

def make_form(model):
    return type(f'{model.__name__}Form', (BaseForm,), {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})

CasoJuridicoForm = make_form(CasoJuridico)
DictamenJuridicoForm = make_form(DictamenJuridico)
NormaLegalForm = make_form(NormaLegal)
ContratoJuridicoForm = make_form(ContratoJuridico)
