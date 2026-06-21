from decimal import Decimal
from clientes_app.models import (
    CompraModel,
    DetalleCompraModel,
    ProductoModel,
    ProveedorModel,
    UsuarioModel,
)
from core.domain.entities.compra import Compra
from core.domain.entities.detalle_compra import DetalleCompra
from django.db.models import Q


class DjangoCompraRepository:
    ESTADOS_AFECTAN_STOCK = ["PENDIENTE", "PAGADA"]

    def _detalle_to_domain(self, obj: DetalleCompraModel) -> DetalleCompra:
        return DetalleCompra(
            id=obj.id,
            compra_id=obj.compra.id if obj.compra else None,
            producto_id=obj.producto.id if obj.producto else None,
            producto_nombre=obj.producto.nombre if obj.producto else None,
            precio_unitario=obj.precio_unitario,
            cantidad=obj.cantidad,
            subtotal=obj.subtotal,
        )

    def _to_domain(self, obj: CompraModel) -> Compra:
        detalles = [self._detalle_to_domain(d) for d in obj.detalles.all()]
        return Compra(
            id=obj.id,
            numero_compra=obj.numero_compra,
            fecha_compra=obj.fecha_compra,
            fecha_estimada_entrega=obj.fecha_estimada_entrega,
            proveedor_id=obj.proveedor.id if obj.proveedor else None,
            proveedor_nombre=obj.proveedor.razon_social if obj.proveedor else None,
            usuario_id=obj.usuario.id if obj.usuario else None,
            usuario_nombre=obj.usuario.nombre if obj.usuario else None,
            estado=obj.estado,
            observaciones=obj.observaciones,
            total=obj.total,
            detalles=detalles,
            activo=obj.activo,
        )

    def _generar_numero_compra(self):
        ultima = CompraModel.objects.order_by("-id").first()

        if not ultima:
            return "COMP-0001"

        try:
            numero = int(ultima.numero_compra.split("-")[1]) + 1
        except Exception:
            numero = ultima.id + 1

        return f"COMP-{numero:04d}"

    def _sumar_stock_por_detalles(self, detalles):
        for det in detalles:
            producto = ProductoModel.objects.get(id=det.producto_id)
            stock_actual = producto.cantidad or 0
            producto.cantidad = stock_actual + det.cantidad
            producto.save()

    def _restar_stock_por_detalles_model(self, detalles_model):
        for det in detalles_model:
            producto = det.producto
            stock_actual = producto.cantidad or 0
            producto.cantidad = stock_actual - det.cantidad
            if producto.cantidad < 0:
                producto.cantidad = 0
            producto.save()

    def crear(self, compra: Compra):
        numero_compra = self._generar_numero_compra()
        proveedor = ProveedorModel.objects.get(id=compra.proveedor_id)
        usuario = UsuarioModel.objects.get(id=compra.usuario_id)

        obj = CompraModel.objects.create(
            numero_compra=numero_compra,
            fecha_compra=compra.fecha_compra,
            fecha_estimada_entrega=compra.fecha_estimada_entrega,
            proveedor=proveedor,
            usuario=usuario,
            estado=compra.estado,
            observaciones=compra.observaciones,
            total=Decimal("0.00"),
            activo=compra.activo if compra.activo is not None else True,
        )

        total = Decimal("0.00")

        for det in compra.detalles:
            producto = ProductoModel.objects.get(id=det.producto_id)
            subtotal = Decimal(det.precio_unitario) * det.cantidad

            DetalleCompraModel.objects.create(
                compra=obj,
                producto=producto,
                precio_unitario=det.precio_unitario,
                cantidad=det.cantidad,
                subtotal=subtotal,
            )
            total += subtotal

        obj.total = total
        obj.save()

        if obj.estado in self.ESTADOS_AFECTAN_STOCK:
            self._sumar_stock_por_detalles(compra.detalles)

        obj = CompraModel.objects.select_related("proveedor", "usuario").prefetch_related("detalles__producto").get(id=obj.id)
        return self._to_domain(obj)

    def listar(self):
        qs = CompraModel.objects.select_related("proveedor", "usuario").prefetch_related("detalles__producto").all().order_by("id")
        return [self._to_domain(obj) for obj in qs]

    def filtrar(self, fecha_desde=None, fecha_hasta=None, proveedor_id=None):
        qs = (
            CompraModel.objects
            .select_related("proveedor", "usuario")
            .prefetch_related("detalles__producto")
            .filter(activo=True)
            .order_by("id")
        )

        if fecha_desde:
            qs = qs.filter(fecha_compra__gte=fecha_desde)

        if fecha_hasta:
            qs = qs.filter(fecha_compra__lte=fecha_hasta)

        if proveedor_id:
            qs = qs.filter(proveedor_id=proveedor_id)

        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, compra_id: int):
        try:
            obj = CompraModel.objects.select_related("proveedor", "usuario").prefetch_related("detalles__producto").get(id=compra_id)
            return self._to_domain(obj)
        except CompraModel.DoesNotExist:
            raise RuntimeError(f"Compra no encontrada: {compra_id}")

    def actualizar(self, compra_id: int, compra: Compra):
        try:
            obj = CompraModel.objects.prefetch_related("detalles__producto").get(id=compra_id)
        except CompraModel.DoesNotExist:
            raise RuntimeError(f"Compra no encontrada: {compra_id}")

        proveedor = ProveedorModel.objects.get(id=compra.proveedor_id)
        usuario = UsuarioModel.objects.get(id=compra.usuario_id)

        estado_anterior = obj.estado
        detalles_anteriores = list(obj.detalles.all())

        if estado_anterior in self.ESTADOS_AFECTAN_STOCK:
            self._restar_stock_por_detalles_model(detalles_anteriores)

        obj.fecha_compra = compra.fecha_compra
        obj.fecha_estimada_entrega = compra.fecha_estimada_entrega
        obj.proveedor = proveedor
        obj.usuario = usuario
        obj.estado = compra.estado
        obj.observaciones = compra.observaciones
        obj.activo = compra.activo

        obj.detalles.all().delete()

        total = Decimal("0.00")
        for det in compra.detalles:
            producto = ProductoModel.objects.get(id=det.producto_id)
            subtotal = Decimal(det.precio_unitario) * det.cantidad

            DetalleCompraModel.objects.create(
                compra=obj,
                producto=producto,
                precio_unitario=det.precio_unitario,
                cantidad=det.cantidad,
                subtotal=subtotal,
            )
            total += subtotal

        obj.total = total
        obj.save()

        if obj.estado in self.ESTADOS_AFECTAN_STOCK:
            self._sumar_stock_por_detalles(compra.detalles)

        obj = CompraModel.objects.select_related("proveedor", "usuario").prefetch_related("detalles__producto").get(id=obj.id)
        return self._to_domain(obj)

    def eliminar(self, compra_id: int):
        try:
            obj = CompraModel.objects.get(id=compra_id)
        except CompraModel.DoesNotExist:
            raise RuntimeError(f"Compra no encontrada: {compra_id}")

        obj.activo = False
        obj.save()

    def activar(self, compra_id):
        obj = CompraModel.objects.get(id=compra_id)
        obj.activo = True
        obj.save()
        return obj