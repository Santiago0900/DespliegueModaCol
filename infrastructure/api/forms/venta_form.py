from django import forms
from clientes_app.models import ClienteModel, UsuarioModel


TIPOS_DOCUMENTO_VENTA = [
    ("FACTURA_VENTA", "FACTURA_VENTA"),
    ("BOLETA", "BOLETA"),
    ("RECIBO", "RECIBO"),
]

FORMAS_PAGO_VENTA = [
    ("CONTADO", "CONTADO"),
    ("CREDITO_30", "CREDITO_30"),
    ("CREDITO_60", "CREDITO_60"),
]

ESTADOS_VENTA = [
    ("BORRADOR", "BORRADOR"),
    ("CONFIRMADA", "CONFIRMADA"),
    ("PAGADA", "PAGADA"),
    ("ANULADA", "ANULADA"),
]


class VentaForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    numero_venta = forms.CharField(required=False, widget=forms.HiddenInput())
    fecha_venta = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control form-control-sm", "type": "date"})
    )
    cliente_id = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    usuario_id = forms.ChoiceField(
        widget=forms.HiddenInput(),  # 🔥 oculto para que sí viaje en el POST
        required=False
    )
    tipo_documento = forms.ChoiceField(
        choices=TIPOS_DOCUMENTO_VENTA,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    forma_pago = forms.ChoiceField(
        choices=FORMAS_PAGO_VENTA,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    estado = forms.ChoiceField(
        choices=ESTADOS_VENTA,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"})
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 3})
    )
    activo = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        usuario_logueado_id = kwargs.pop("usuario_logueado_id", None)
        super().__init__(*args, **kwargs)

        self.usuario_logueado_nombre = ""

        self.fields["cliente_id"].choices = [("", "-- Seleccione Cliente --")] + [
            (c.id, c.nombre) for c in ClienteModel.objects.filter(activo=True).order_by("id")
        ]

        if usuario_logueado_id:
            usuarios = UsuarioModel.objects.filter(id=usuario_logueado_id, activo=True).order_by("id")
            usuario = usuarios.first()

            if usuario:
                self.fields["usuario_id"].choices = [(usuario.id, usuario.nombre)]
                self.fields["usuario_id"].initial = usuario.id
                self.usuario_logueado_nombre = usuario.nombre
            else:
                self.fields["usuario_id"].choices = []
        else:
            self.fields["usuario_id"].choices = [
                (u.id, u.nombre) for u in UsuarioModel.objects.filter(activo=True).order_by("id")
            ]