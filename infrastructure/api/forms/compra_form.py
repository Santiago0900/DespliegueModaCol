from django import forms
from clientes_app.models import ProveedorModel, UsuarioModel


ESTADOS_COMPRA = [
    ("PENDIENTE", "Pendiente"),
    ("PAGADA", "Pagada"),
    ("ANULADA", "Anulada"),
]


class CompraForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    numero_compra = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "readonly": True
        })
    )

    fecha_compra = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control form-control-sm",
            "type": "date"
        })
    )

    fecha_estimada_entrega = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "class": "form-control form-control-sm",
            "type": "date"
        })
    )

    proveedor_id = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    # este es el que viaja en el POST
    usuario_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )

    # este solo muestra el nombre en pantalla
    usuario_nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "readonly": True
        })
    )

    estado = forms.ChoiceField(
        choices=ESTADOS_COMPRA,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control form-control-sm",
            "rows": 2
        })
    )

    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        usuario_logueado_id = kwargs.pop("usuario_logueado_id", None)
        usuario_logueado_nombre = kwargs.pop("usuario_logueado_nombre", "")
        super().__init__(*args, **kwargs)

        self.fields["proveedor_id"].choices = [("", "-- Seleccione Proveedor --")] + [
            (p.id, p.razon_social)
            for p in ProveedorModel.objects.filter(activo=True).order_by("id")
        ]

        if usuario_logueado_id:
            self.fields["usuario_id"].initial = usuario_logueado_id
            self.fields["usuario_nombre"].initial = usuario_logueado_nombre
        elif not self.initial.get("usuario_id"):
            primer_usuario = UsuarioModel.objects.filter(activo=True).order_by("id").first()
            if primer_usuario:
                self.fields["usuario_id"].initial = primer_usuario.id
                self.fields["usuario_nombre"].initial = primer_usuario.nombre