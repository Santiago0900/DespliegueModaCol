from django.db import models
from django.utils import timezone
from datetime import timedelta

class PasswordResetTokenModel(models.Model):
    usuario = models.ForeignKey(
        'UsuarioModel',
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        db_column='usuario_id'
    )
    token = models.CharField(max_length=255, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    class Meta:
        db_table = "password_reset_tokens"
        ordering = ["-id"]

    def expiro(self):
        return timezone.now() > self.creado_en + timedelta(hours=1)

    def __str__(self):
        return f"{self.usuario_id} - {self.token}"

class ModuloModel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "modulos"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

class RolModel(models.Model):
    tipo = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "roles"
        ordering = ["id"]

    def __str__(self):
        return self.tipo

class RolPermisoModel(models.Model):
    rol = models.ForeignKey(
        'RolModel',
        on_delete=models.CASCADE,
        related_name='permisos',
        db_column='rol_id'
    )
    modulo = models.ForeignKey(
        'ModuloModel',
        on_delete=models.CASCADE,
        related_name='roles',
        db_column='modulo_id'
    )
    puede_ver = models.BooleanField(default=True)
    puede_crear = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)

    class Meta:
        db_table = "roles_permisos"
        unique_together = ("rol", "modulo")
        ordering = ["id"]

    def __str__(self):
        return f"{self.rol.tipo} - {self.modulo.codigo}"


class VentaModel(models.Model):
    numero_venta = models.CharField(max_length=20, unique=True)
    fecha_venta = models.DateField()
    cliente = models.ForeignKey(
        'ClienteModel',
        on_delete=models.PROTECT,
        db_column="cliente_id",
        related_name="ventas",
    )
    usuario = models.ForeignKey(
        'UsuarioModel',
        on_delete=models.PROTECT,
        db_column="usuario_id",
        related_name="ventas",
    )
    tipo_documento = models.CharField(max_length=30)
    forma_pago = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "ventas"
        ordering = ["id"]

    def __str__(self):
        return self.numero_venta


class DetalleVentaModel(models.Model):
    venta = models.ForeignKey(
        'VentaModel',
        on_delete=models.CASCADE,
        db_column="venta_id",
        related_name="detalles",
    )
    producto = models.ForeignKey(
        'ProductoModel',
        on_delete=models.PROTECT,
        db_column="producto_id",
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "detalle_ventas"
        ordering = ["id"]

    def __str__(self):
        return f"{self.venta_id} - {self.producto_id}"


class FlujoCajaModel(models.Model):
    TIPO_INGRESO = "INGRESO"
    TIPO_EGRESO = "EGRESO"
    TIPOS = [
        (TIPO_INGRESO, "INGRESO"),
        (TIPO_EGRESO, "EGRESO"),
    ]

    fecha = models.DateField()
    tipo_movimiento = models.CharField(max_length=10, choices=TIPOS)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    venta_id = models.BigIntegerField(blank=True, null=True)
    compra_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = "flujo_caja"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto}"


class CompraModel(models.Model):
    numero_compra = models.CharField(max_length=30, unique=True)
    fecha_compra = models.DateField()
    fecha_estimada_entrega = models.DateField(blank=True, null=True)

    proveedor = models.ForeignKey(
        "ProveedorModel",
        on_delete=models.PROTECT,
        db_column="proveedor_id",
        related_name="compras"
    )
    usuario = models.ForeignKey(
        "UsuarioModel",
        on_delete=models.PROTECT,
        db_column="usuario_id",
        related_name="compras"
    )

    estado = models.CharField(max_length=20, default="PENDIENTE")
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "compras"
        ordering = ["id"]

    def __str__(self):
        return self.numero_compra


class DetalleCompraModel(models.Model):
    compra = models.ForeignKey(
        "CompraModel",
        on_delete=models.CASCADE,
        db_column="compra_id",
        related_name="detalles"
    )
    producto = models.ForeignKey(
        "ProductoModel",
        on_delete=models.PROTECT,
        db_column="producto_id"
    )
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "detalle_compras"
        ordering = ["id"]

    def __str__(self):
        return f"{self.compra_id} - {self.producto_id}"


class ProveedorModel(models.Model):
    razon_social = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "proveedores"
        ordering = ["id"]

    def __str__(self):
        return self.razon_social


class ProductoModel(models.Model):
    fecha = models.DateField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    proveedor = models.ForeignKey(
        'ProveedorModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="proveedor_id"
    )
    categoria = models.ForeignKey(
        'CategoriaModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos',
        db_column='categoria_id'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "productos"
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class ClienteModel(models.Model):
    empresa = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    contacto = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "clientes"
        ordering = ["id"]

    def __str__(self):
        return f"{self.empresa} - {self.nombre}"


class CategoriaModel(models.Model):
    tipo_categoria = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "categorias"
        ordering = ["id"]

    def __str__(self):
        return self.tipo_categoria


class UsuarioModel(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=200)
    rol = models.ForeignKey('RolModel', on_delete=models.PROTECT, db_column="id_rol")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "usuarios"
        ordering = ["id"]

    def __str__(self):
        return self.nombre

    def tiene_permiso(self, modulo_codigo, accion):
        try:
            permiso = self.rol.permisos.get(modulo__codigo=modulo_codigo)

            if accion == "ver":
                return permiso.puede_ver
            elif accion == "crear":
                return permiso.puede_crear
            elif accion == "editar":
                return permiso.puede_editar
            elif accion == "eliminar":
                return permiso.puede_eliminar
            return False
        except:
            return False

class MensajeModel(models.Model):
    remitente = models.ForeignKey(
        'UsuarioModel',
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        db_column='remitente_id'
    )
    destinatario = models.ForeignKey(
        'UsuarioModel',
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos',
        db_column='destinatario_id'
    )
    asunto = models.CharField(max_length=100)
    contenido = models.TextField(max_length=1000)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        db_table = "mensajes"
        ordering = ["-fecha_envio"]

    def __str__(self):
        return f"{self.asunto} - {self.remitente_id} -> {self.destinatario_id}"