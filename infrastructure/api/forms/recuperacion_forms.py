from django import forms


class SolicitarRecuperacionForm(forms.Form):
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu correo"
        })
    )


class RestablecerPasswordForm(forms.Form):
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Nueva contraseña"
        })
    )
    confirm_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirmar contraseña"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data