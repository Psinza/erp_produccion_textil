# apps/tesoreria/forms.py
from django import forms
from .models import (
    Banco, CuentaBancaria, MovimientoBancario,
    Caja, MovimientoCaja,
    CuentaPorCobrar, CuentaPorPagar,
    Cobro, Pago, TransferenciaBancaria,
    MovimientoTesoreria,
)

CTR  = {"class": "form-control"}
SEL  = {"class": "form-select"}
NUM  = {"class": "form-control", "step": "0.01"}
DATE = {"class": "form-control", "type": "date"}
CHK  = {"class": "form-check-input"}
TXT  = {"class": "form-control", "rows": 3}


class BancoForm(forms.ModelForm):
    class Meta:
        model   = Banco
        fields  = ["nombre", "codigo", "pais", "activo"]
        widgets = {
            "nombre": forms.TextInput(attrs=CTR),
            "codigo": forms.TextInput(attrs=CTR),
            "pais":   forms.TextInput(attrs=CTR),
            "activo": forms.CheckboxInput(attrs=CHK),
        }


class CuentaBancariaForm(forms.ModelForm):
    class Meta:
        model  = CuentaBancaria
        fields = [
            "banco", "numero", "alias", "tipo", "moneda",
            "saldo_inicial", "titular", "activa",
        ]
        widgets = {
            "banco":         forms.Select(attrs=SEL),
            "numero":        forms.TextInput(attrs=CTR),
            "alias":         forms.TextInput(attrs=CTR),
            "tipo":          forms.Select(attrs=SEL),
            "moneda":        forms.Select(attrs=SEL),
            "saldo_inicial": forms.NumberInput(attrs=NUM),
            "titular":       forms.TextInput(attrs=CTR),
            "activa":        forms.CheckboxInput(attrs=CHK),
        }


class MovimientoBancarioForm(forms.ModelForm):
    class Meta:
        model  = MovimientoBancario
        fields = ["cuenta", "fecha", "tipo", "concepto", "pago", "monto_igtf",
              "descripcion", "referencia", "monto", "conciliado"]
        widgets = {
            "cuenta":      forms.Select(attrs=SEL),
            "fecha":       forms.DateInput(attrs=DATE),
            "tipo":        forms.Select(attrs=SEL),
            "concepto":    forms.Select(attrs=SEL),
            "descripcion": forms.TextInput(attrs=CTR),
            "referencia":  forms.TextInput(attrs=CTR),
            "monto":       forms.NumberInput(attrs=NUM),
            "monto_igtf":  forms.NumberInput(attrs=NUM),
            "conciliado": forms.CheckboxInput(attrs=CHK),
        }


class CajaForm(forms.ModelForm):
    class Meta:
        model  = Caja
        fields = ["nombre", "responsable", "monto_asignado", "activa"]
        widgets = {
            "nombre":         forms.TextInput(attrs=CTR),
            "responsable":    forms.Select(attrs=SEL),
            "monto_asignado": forms.NumberInput(attrs=NUM),
            "activa":         forms.CheckboxInput(attrs=CHK),
        }


class MovimientoCajaForm(forms.ModelForm):
    class Meta:
        model  = MovimientoCaja
        fields = ["caja", "fecha", "tipo", "descripcion", "monto", "comprobante"]
        widgets = {
            "caja":        forms.Select(attrs=SEL),
            "fecha":       forms.DateInput(attrs=DATE),
            "tipo":        forms.Select(attrs=SEL),
            "descripcion": forms.TextInput(attrs=CTR),
            "monto":       forms.NumberInput(attrs=NUM),
            "comprobante": forms.TextInput(attrs=CTR),
        }


class CuentaPorCobrarForm(forms.ModelForm):
    class Meta:
        model  = CuentaPorCobrar
        fields = [
            "cliente_nombre", "cliente_ruc", "concepto", "referencia",
            "fecha_emision", "fecha_vencimiento", "monto_total", "observaciones",
        ]
        widgets = {
            "cliente_nombre":   forms.TextInput(attrs=CTR),
            "cliente_ruc":      forms.TextInput(attrs=CTR),
            "concepto":         forms.TextInput(attrs=CTR),
            "referencia":       forms.TextInput(attrs=CTR),
            "fecha_emision":    forms.DateInput(attrs=DATE),
            "fecha_vencimiento":forms.DateInput(attrs=DATE),
            "monto_total":      forms.NumberInput(attrs=NUM),
            "observaciones":    forms.Textarea(attrs=TXT),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("fecha_emision") and cleaned.get("fecha_vencimiento") and cleaned["fecha_vencimiento"] < cleaned["fecha_emision"]:
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de emisión.")
        return cleaned


class CuentaPorPagarForm(forms.ModelForm):
    class Meta:
        model  = CuentaPorPagar
        fields = [
            "proveedor_nombre", "proveedor_ruc", "concepto", "referencia",
            "fecha_emision", "fecha_vencimiento", "monto_total", "observaciones",
        ]
        widgets = {
            "proveedor_nombre":  forms.TextInput(attrs=CTR),
            "proveedor_ruc":     forms.TextInput(attrs=CTR),
            "concepto":          forms.TextInput(attrs=CTR),
            "referencia":        forms.TextInput(attrs=CTR),
            "fecha_emision":     forms.DateInput(attrs=DATE),
            "fecha_vencimiento": forms.DateInput(attrs=DATE),
            "monto_total":       forms.NumberInput(attrs=NUM),
            "observaciones":     forms.Textarea(attrs=TXT),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("fecha_emision") and cleaned.get("fecha_vencimiento") and cleaned["fecha_vencimiento"] < cleaned["fecha_emision"]:
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de emisión.")
        return cleaned


class CobroForm(forms.ModelForm):
    class Meta:
        model  = Cobro
        fields = ["fecha", "monto", "medio_pago", "cuenta_bancaria",
                  "referencia", "observaciones"]
        widgets = {
            "fecha":           forms.DateInput(attrs=DATE),
            "monto":           forms.NumberInput(attrs=NUM),
            "medio_pago":      forms.Select(attrs=SEL),
            "cuenta_bancaria": forms.Select(attrs=SEL),
            "referencia":      forms.TextInput(attrs=CTR),
            "observaciones":   forms.TextInput(attrs=CTR),
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model  = Pago
        fields = ["fecha", "monto", "medio_pago", "cuenta_bancaria",
                  "referencia", "observaciones"]
        widgets = {
            "fecha":           forms.DateInput(attrs=DATE),
            "monto":           forms.NumberInput(attrs=NUM),
            "medio_pago":      forms.Select(attrs=SEL),
            "cuenta_bancaria": forms.Select(attrs=SEL),
            "referencia":      forms.TextInput(attrs=CTR),
            "observaciones":   forms.TextInput(attrs=CTR),
        }


class TransferenciaBancariaForm(forms.ModelForm):
    class Meta:
        model  = TransferenciaBancaria
        fields = ["cuenta_origen", "cuenta_destino", "fecha",
                  "monto", "descripcion", "referencia"]
        widgets = {
            "cuenta_origen":  forms.Select(attrs=SEL),
            "cuenta_destino": forms.Select(attrs=SEL),
            "fecha":          forms.DateInput(attrs=DATE),
            "monto":          forms.NumberInput(attrs=NUM),
            "descripcion":    forms.TextInput(attrs=CTR),
            "referencia":     forms.TextInput(attrs=CTR),
        }

    def clean(self):
        cd = super().clean()
        if cd.get("cuenta_origen") == cd.get("cuenta_destino"):
            raise forms.ValidationError(
                "La cuenta de origen y destino no pueden ser la misma."
            )
        return cd


class MovimientoTesoreriaForm(forms.ModelForm):
    class Meta:
        model = MovimientoTesoreria
        fields = ['fecha', 'tipo', 'concepto', 'monto', 'cuenta', 'caja', 'referencia', 'observaciones']
        widgets = {'fecha': forms.DateInput(attrs=DATE), 'observaciones': forms.Textarea(attrs=TXT)}
