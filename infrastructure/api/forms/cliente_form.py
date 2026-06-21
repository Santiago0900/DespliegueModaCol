from django import forms
from clientes_app.models import ClienteModel
import re


class ClienteForm(forms.ModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ClienteModel
        fields = ["id", "empresa", "nombre", "identificacion", "contacto", "correo", "activo"]
        widgets = {
            "empresa": forms.TextInput(attrs={
                "class": "form-control input-custom",
                "placeholder": "Ej: Modacol SAS",
                "maxlength": 100,
                "autocomplete": "organization",
            }),
            "nombre": forms.TextInput(attrs={
                "class": "form-control input-custom",
                "placeholder": "Ej: Didier Torres",
                "maxlength": 100,
                "autocomplete": "name",
            }),
            "identificacion": forms.TextInput(attrs={
                "class": "form-control input-custom",
                "placeholder": "Solo números",
                "maxlength": 20,
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "autocomplete": "off",
                "oninput": "this.value = this.value.replace(/[^0-9]/g, '')",
            }),
            "contacto": forms.TextInput(attrs={
                "class": "form-control input-custom",
                "placeholder": "Ej: 3001234567",
                "maxlength": 15,
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "autocomplete": "tel",
                "oninput": "this.value = this.value.replace(/[^0-9]/g, '')",
            }),
            "correo": forms.EmailInput(attrs={
                "class": "form-control input-custom",
                "placeholder": "cliente@correo.com",
                "maxlength": 100,
                "autocomplete": "email",
            }),
        }

    def clean_empresa(self):
        empresa = self.cleaned_data.get("empresa", "").strip()

        if not empresa:
            raise forms.ValidationError("La empresa es obligatoria")

        if len(empresa) < 2:
            raise forms.ValidationError("La empresa debe tener al menos 2 caracteres")

        if len(empresa) > 100:
            raise forms.ValidationError("La empresa no puede exceder 100 caracteres")

        if not re.match(r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.\-]+$", empresa):
            raise forms.ValidationError("La empresa contiene caracteres inválidos")

        return empresa

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio")

        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres")

        if len(nombre) > 100:
            raise forms.ValidationError("El nombre no puede exceder 100 caracteres")

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise forms.ValidationError("El nombre solo puede contener letras")

        return nombre

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get("identificacion", "").strip()

        if not identificacion:
            raise forms.ValidationError("La identificación es obligatoria")

        if len(identificacion) < 5:
            raise forms.ValidationError("La identificación es demasiado corta")

        if len(identificacion) > 20:
            raise forms.ValidationError("La identificación no puede exceder 20 caracteres")

        if not re.match(r"^[0-9]+$", identificacion):
            raise forms.ValidationError("La identificación solo puede contener números")

        qs = ClienteModel.objects.filter(identificacion=identificacion)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un cliente con esta identificación")

        return identificacion

    def clean_contacto(self):
        contacto = self.cleaned_data.get("contacto")

        if contacto:
            contacto = contacto.strip()

            if not re.match(r"^[0-9]{7,15}$", contacto):
                raise forms.ValidationError("El contacto debe tener entre 7 y 15 dígitos y solo números")

        return contacto

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")

        if correo:
            correo = correo.strip().lower()

            if len(correo) > 100:
                raise forms.ValidationError("El correo no puede exceder 100 caracteres")

            qs = ClienteModel.objects.filter(correo=correo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Ya existe un cliente con este correo")

        return correo

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")
        empresa = cleaned_data.get("empresa")

        if nombre and empresa and nombre.lower() in empresa.lower():
            self.add_error("nombre", "El nombre no debe estar contenido dentro de la empresa")

        return cleaned_data