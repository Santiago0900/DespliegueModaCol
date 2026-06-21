from decimal import Decimal

from clientes_app.models import ( VentaModel, DetalleVentaModel, ProductoModel, ClienteModel, UsuarioModel, )
from core.domain.entities.venta import Venta
from core.domain.entities.detalle_venta import DetalleVenta


IVA = Decimal("0.19")


class DjangoVentaRepository:
    def _detalle_to_domain(self, obj: DetalleVentaModel) -> DetalleVenta:
        return DetalleVenta(
            id=obj.id,
            venta_id=obj.venta.id if obj.venta else None,
            producto_id=obj.producto.id if obj.producto else None,
            producto_nombre=obj.producto.nombre if obj.producto else None,
            cantidad=obj.cantidad,
            precio_unitario=obj.precio_unitario,
            subtotal=obj.subtotal,
        )

    def _to_domain(self, obj: VentaModel) -> Venta:
        detalles = [self._detalle_to_domain(d) for d in obj.detalles.all()]
        return Venta(
            id=obj.id,
            numero_venta=obj.numero_venta,
            fecha_venta=obj.fecha_venta,
            cliente_id=obj.cliente.id if obj.cliente else None,
            usuario_id=obj.usuario.id if obj.usuario else None,
            cliente_nombre=obj.cliente.nombre if obj.cliente else None,
            usuario_nombre=obj.usuario.nombre if obj.usuario else None,
            tipo_documento=obj.tipo_documento,
            forma_pago=obj.forma_pago,
            estado=obj.estado,
            observaciones=obj.observaciones,
            total=obj.total,
            detalles=detalles,
            activo=obj.activo,
        )

    def _generar_numero_venta(self):
        ultima = VentaModel.objects.order_by("-id").first()
        if not ultima:
            return "V-000001"

        try:
            ultimo_numero = int(ultima.numero_venta.split("-")[1])
        except Exception:
            ultimo_numero = ultima.id

        siguiente = ultimo_numero + 1
        return f"V-{siguiente:06d}"

    def _calcular_subtotal_con_iva(self, precio, cantidad):
        base = Decimal(precio) * int(cantidad)
        iva = base * IVA
        return base + iva

    def _validar_stock(self, detalles):
        for d in detalles:
            producto = ProductoModel.objects.get(id=d.producto_id)
            stock_actual = producto.cantidad or 0

            if d.cantidad <= 0:
                raise RuntimeError(f"La cantidad debe ser mayor a 0 para {producto.nombre}")

            if Decimal(d.precio_unitario) <= 0:
                raise RuntimeError(f"El precio debe ser mayor a 0 para {producto.nombre}")

            if d.cantidad > stock_actual:
                raise RuntimeError(
                    f"Stock insuficiente para {producto.nombre}. "
                    f"Disponible: {stock_actual}, solicitado: {d.cantidad}"
                )

    def crear(self, venta: Venta):
        cliente = ClienteModel.objects.get(id=venta.cliente_id)
        usuario = UsuarioModel.objects.get(id=venta.usuario_id)

        numero_venta = venta.numero_venta or self._generar_numero_venta()

        if not venta.detalles:
            raise RuntimeError("La venta debe tener al menos un producto.")

        self._validar_stock(venta.detalles)

        obj = VentaModel.objects.create(
            numero_venta=numero_venta,
            fecha_venta=venta.fecha_venta,
            cliente=cliente,
            usuario=usuario,
            tipo_documento=venta.tipo_documento,
            forma_pago=venta.forma_pago,
            estado=venta.estado,
            observaciones=venta.observaciones,
            total=Decimal("0.00"),
            activo=venta.activo if venta.activo is not None else True,
        )

        total = Decimal("0.00")

        for det in venta.detalles:
            producto = ProductoModel.objects.get(id=det.producto_id)
            subtotal = self._calcular_subtotal_con_iva(det.precio_unitario, det.cantidad)

            DetalleVentaModel.objects.create(
                venta=obj,
                producto=producto,
                cantidad=det.cantidad,
                precio_unitario=det.precio_unitario,
                subtotal=subtotal,
            )

            total += subtotal

            if obj.estado in ["CONFIRMADA", "PAGADA"]:
                stock_actual = producto.cantidad or 0
                producto.cantidad = stock_actual - det.cantidad
                producto.save()

        obj.total = total
        obj.save()

        obj = (
            VentaModel.objects
            .select_related("cliente", "usuario")
            .prefetch_related("detalles__producto")
            .get(id=obj.id)
        )
        return self._to_domain(obj)

    def listar(self):
        qs = (
            VentaModel.objects
            .select_related("cliente", "usuario")
            .prefetch_related("detalles__producto")
            .all()
            .order_by("-id")
        )
        return [self._to_domain(obj) for obj in qs]

    def filtrar(self, fecha_inicio=None, fecha_fin=None, cliente_id=None):
        qs = (
            VentaModel.objects
            .select_related("cliente", "usuario")
            .prefetch_related("detalles__producto")
            .all()
            .order_by("-id")
        )

        if fecha_inicio:
            qs = qs.filter(fecha_venta__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha_venta__lte=fecha_fin)
        if cliente_id:
            qs = qs.filter(cliente_id=cliente_id)

        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, venta_id: int):
        try:
            obj = (
                VentaModel.objects
                .select_related("cliente", "usuario")
                .prefetch_related("detalles__producto")
                .get(id=venta_id)
            )
            return self._to_domain(obj)
        except VentaModel.DoesNotExist:
            raise RuntimeError(f"Venta no encontrada: {venta_id}")

    def actualizar(self, venta_id: int, venta: Venta):
        try:
            obj = VentaModel.objects.get(id=venta_id)
        except VentaModel.DoesNotExist:
            raise RuntimeError(f"Venta no encontrada: {venta_id}")

        cliente = ClienteModel.objects.get(id=venta.cliente_id)
        usuario = UsuarioModel.objects.get(id=venta.usuario_id)

        obj.fecha_venta = venta.fecha_venta
        obj.cliente = cliente
        obj.usuario = usuario
        obj.tipo_documento = venta.tipo_documento
        obj.forma_pago = venta.forma_pago
        obj.estado = venta.estado
        obj.observaciones = venta.observaciones
        obj.activo = venta.activo

        obj.detalles.all().delete()

        total = Decimal("0.00")
        for det in venta.detalles:
            producto = ProductoModel.objects.get(id=det.producto_id)
            subtotal = self._calcular_subtotal_con_iva(det.precio_unitario, det.cantidad)

            DetalleVentaModel.objects.create(
                venta=obj,
                producto=producto,
                cantidad=det.cantidad,
                precio_unitario=det.precio_unitario,
                subtotal=subtotal,
            )
            total += subtotal

        obj.total = total
        obj.save()

        obj = (
            VentaModel.objects
            .select_related("cliente", "usuario")
            .prefetch_related("detalles__producto")
            .get(id=obj.id)
        )
        return self._to_domain(obj)

    def eliminar(self, venta_id: int):
        try:
            obj = VentaModel.objects.get(id=venta_id)
        except VentaModel.DoesNotExist:
            raise RuntimeError(f"Venta no encontrada: {venta_id}")

        obj.activo = False
        obj.save()

    def activar(self, venta_id: int):
        try:
            obj = VentaModel.objects.get(id=venta_id)
        except VentaModel.DoesNotExist:
            raise RuntimeError("Venta no encontrado")

        obj.activo = True
        obj.save()