from django import forms
from clientes_app.models import UsuarioModel, RolModel
import re


class UsuarioForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"})
    )
    correo = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={"class": "form-control form-control-sm"})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm"})
    )
    rol_id = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rol_id"].choices = [("", "-- Seleccione rol --")] + [
            (rol.id, rol.tipo)
            for rol in RolModel.objects.filter(activo=True).order_by("id")
        ]

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio")
        if len(nombre) > 100:
            raise forms.ValidationError("El nombre no puede exceder 100 caracteres")
        if not re.match(r"^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios")
        return nombre

    def clean_correo(self):
        correo = self.cleaned_data.get("correo", "").strip().lower()
        if not correo:
            raise forms.ValidationError("El correo es obligatorio")

        usuario_id = self.cleaned_data.get("id")
        qs = UsuarioModel.objects.filter(correo=correo)
        if usuario_id:
            qs = qs.exclude(id=usuario_id)

        if qs.exists():
            raise forms.ValidationError("Ya existe un usuario con este correo")

        return correo

    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        usuario_id = self.cleaned_data.get("id")

        if not usuario_id and not password:
            raise forms.ValidationError("La contraseña es obligatoria al crear un usuario")

        if password:
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password):
                raise forms.ValidationError("La contraseña debe contener al menos una letra y un número")

        return password

    def clean_rol_id(self):
        rol_id = self.cleaned_data.get("rol_id")
        if not rol_id:
            raise forms.ValidationError("El rol es obligatorio")
        return rol_id