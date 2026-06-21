from django import forms


class LoginForm(forms.Form):
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña",
            "autocomplete": "current-password",
        })
    )