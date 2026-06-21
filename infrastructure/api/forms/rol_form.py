from django import forms
from clientes_app.models import RolModel
import re

class RolForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    tipo = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"})
    )
    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())


    def clean_tipo(self):
        tipo = self.cleaned_data.get("tipo", "").strip().upper()

        if not tipo:
            raise forms.ValidationError("El tipo de rol es obligatorio")
        if len(tipo) > 50:
            raise forms.ValidationError("El tipo de rol no puede exceder 50 caracteres")
        if not re.match(r"^[A-ZÁÉÍÓÚÑ_\s]+$", tipo):
            raise forms.ValidationError("El rol solo puede contener letras y debe estar en MAYÚSCULAS")

        rol_id = self.cleaned_data.get("id")
        qs = RolModel.objects.filter(tipo=tipo)
        if rol_id:
            qs = qs.exclude(id=rol_id)
        if qs.exists():
            raise forms.ValidationError("Ya existe un rol con ese nombre")

        return tipo

