from django import forms
from clientes_app.models import ProveedorModel
import re


class ProveedorForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    razon_social = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Ej: Comercial Andina",
        })
    )

    identificacion = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Solo números",
            "maxlength": 20,
            "inputmode": "numeric",
            "pattern": "[0-9]*",
            "oninput": "this.value = this.value.replace(/[^0-9]/g, '')",
        })
    )

    direccion = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Dirección",
        })
    )

    correo = forms.EmailField(
        required=False,
        max_length=100,
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "proveedor@correo.com",
        })
    )

    contacto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Solo números",
            "maxlength": 15,
            "inputmode": "numeric",
            "pattern": "[0-9]*",
            "oninput": "this.value = this.value.replace(/[^0-9]/g, '')",
        })
    )

    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def clean_razon_social(self):
        razon_social = self.cleaned_data.get("razon_social", "").strip()

        if not razon_social:
            raise forms.ValidationError("La razón social es obligatoria")

        if len(razon_social) < 3:
            raise forms.ValidationError("La razón social debe tener al menos 3 caracteres")

        if len(razon_social) > 100:
            raise forms.ValidationError("La razón social no puede exceder 100 caracteres")

        # no permitir números
        if re.search(r"\d", razon_social):
            raise forms.ValidationError("La razón social no debe contener números")

        # permitir letras, espacios, puntos, comas, guiones y &
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\,\-&]+$", razon_social):
            raise forms.ValidationError("La razón social contiene caracteres inválidos")

        return razon_social

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get("identificacion", "").strip()

        if not identificacion:
            raise forms.ValidationError("La identificación es obligatoria")

        if len(identificacion) < 8:
            raise forms.ValidationError("La identificación es demasiado corta")

        if len(identificacion) > 20:
            raise forms.ValidationError("La identificación no puede exceder 20 caracteres")

        if not re.match(r"^[0-9]+$", identificacion):
            raise forms.ValidationError("La identificación solo puede contener números")

        proveedor_id = self.cleaned_data.get("id")
        qs = ProveedorModel.objects.filter(identificacion=identificacion)
        if proveedor_id:
            qs = qs.exclude(id=proveedor_id)

        if qs.exists():
            raise forms.ValidationError("Ya existe un proveedor con esta identificación")

        return identificacion

    def clean_direccion(self):
        direccion = self.cleaned_data.get("direccion", "").strip()
        if len(direccion) > 150:
            raise forms.ValidationError("La dirección no puede exceder 150 caracteres")
        return direccion

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        if correo:
            correo = correo.strip().lower()
            if len(correo) > 100:
                raise forms.ValidationError("El correo no puede exceder 100 caracteres")
        return correo

    def clean_contacto(self):
        contacto = self.cleaned_data.get("contacto", "").strip()
        if contacto and not re.match(r"^[0-9]{7,15}$", contacto):
            raise forms.ValidationError("El contacto debe tener entre 7 y 15 dígitos")
        return contacto