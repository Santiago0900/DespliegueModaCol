from django import forms
from datetime import date
from clientes_app.models import ProveedorModel, CategoriaModel


class ProductoForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control form-control-sm", "type": "date"})
    )
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"})
    )
    descripcion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"})
    )
    precio_unitario = forms.DecimalField(
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm", "step": "0.01"})
    )
    cantidad = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"})
    )
    proveedor_id = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    categoria_id = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["proveedor_id"].choices = [("", "-- Seleccione Proveedor --")] + [
            (p.id, p.razon_social)
            for p in ProveedorModel.objects.filter(activo=True).order_by("id")
        ]

        self.fields["categoria_id"].choices = [("", "-- Seleccione Categoría --")] + [
            (c.id, c.tipo_categoria)
            for c in CategoriaModel.objects.filter(activo=True).order_by("id")
        ]

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha > date.today():
            raise forms.ValidationError("La fecha no puede ser futura")
        return fecha

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio")
        if len(nombre) > 100:
            raise forms.ValidationError("El nombre no puede exceder 100 caracteres")
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion", "").strip()
        if len(descripcion) > 500:
            raise forms.ValidationError("La descripción no puede exceder 500 caracteres")
        return descripcion