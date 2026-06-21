from django import forms
from clientes_app.models import CategoriaModel


class CategoriaForm(forms.ModelForm):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = CategoriaModel
        fields = ["id", "tipo_categoria", "activo"]
        widgets = {
            "tipo_categoria": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Ropa, Calzado, Accesorios...",
                "maxlength": 100,
            }),
        }

    def clean_tipo_categoria(self):
        tipo = (self.cleaned_data.get("tipo_categoria") or "").strip()

        if not tipo:
            raise forms.ValidationError("El tipo de categoría es obligatorio")

        if len(tipo) < 3:
            raise forms.ValidationError("La categoría es demasiado corta. Debe tener al menos 3 caracteres")

        if len(tipo) > 100:
            raise forms.ValidationError("La categoría no puede superar los 100 caracteres")

        qs = CategoriaModel.objects.filter(tipo_categoria__iexact=tipo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe una categoría con ese nombre")

        return tipo