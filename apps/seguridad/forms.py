from django import forms

from .models import (
    DotacionEquipo, Guardia, IncidenteSeguridad, InspeccionSST,
    OrdenSalidaMaterial, PaseIngreso, PuestoSeguridad, RegistroAcceso,
    RondaSeguridad, TurnoGuardia,
)


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


class GuardiaForm(BootstrapModelForm):
    class Meta:
        model = Guardia
        fields = '__all__'


class PuestoSeguridadForm(BootstrapModelForm):
    class Meta:
        model = PuestoSeguridad
        fields = '__all__'


class TurnoGuardiaForm(BootstrapModelForm):
    class Meta:
        model = TurnoGuardia
        fields = '__all__'


class DotacionEquipoForm(BootstrapModelForm):
    class Meta:
        model = DotacionEquipo
        exclude = ('registrado_por',)


class PaseIngresoForm(BootstrapModelForm):
    class Meta:
        model = PaseIngreso
        exclude = ('autorizado_por',)


class RegistroAccesoForm(BootstrapModelForm):
    class Meta:
        model = RegistroAcceso
        exclude = ('registrado_por',)


class OrdenSalidaMaterialForm(BootstrapModelForm):
    class Meta:
        model = OrdenSalidaMaterial
        exclude = ('autorizado_por',)


class RondaSeguridadForm(BootstrapModelForm):
    class Meta:
        model = RondaSeguridad
        fields = '__all__'


class IncidenteSeguridadForm(BootstrapModelForm):
    class Meta:
        model = IncidenteSeguridad
        exclude = ('reportado_por',)


class InspeccionSSTForm(BootstrapModelForm):
    class Meta:
        model = InspeccionSST
        fields = '__all__'
