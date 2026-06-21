from core.domain.entities.producto import Producto
from clientes_app.models import ProductoModel, ProveedorModel, CategoriaModel


class DjangoProductoRepository:
    def _to_domain(self, obj: ProductoModel) -> Producto:
        return Producto(
            id=obj.id,
            fecha=obj.fecha,
            nombre=obj.nombre,
            descripcion=obj.descripcion,
            precio_unitario=obj.precio_unitario,
            cantidad=obj.cantidad,
            proveedor_id=obj.proveedor.id if obj.proveedor else None,
            proveedor_nombre=obj.proveedor.razon_social if obj.proveedor else None,
            categoria_id=obj.categoria.id if obj.categoria else None,
            categoria_nombre=obj.categoria.tipo_categoria if obj.categoria else None,
            activo=obj.activo,
        )

    def crear(self, producto: Producto):
        proveedor = None
        categoria = None

        if producto.proveedor_id:
            proveedor = ProveedorModel.objects.get(id=producto.proveedor_id)

        if producto.categoria_id:
            categoria = CategoriaModel.objects.get(id=producto.categoria_id)

        obj = ProductoModel.objects.create(
            fecha=producto.fecha,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio_unitario=producto.precio_unitario,
            cantidad=producto.cantidad,
            proveedor=proveedor,
            categoria=categoria,
            activo=producto.activo if producto.activo is not None else True,
        )
        return self._to_domain(obj)

    def listar(self):
        return [
            self._to_domain(obj)
            for obj in ProductoModel.objects.select_related("proveedor", "categoria").all().order_by("id")
        ]

    def filtrar(self, nombre=None, descripcion=None, proveedor_id=None):
        qs = ProductoModel.objects.select_related("proveedor", "categoria").all().order_by("id")

        if nombre:
            qs = qs.filter(nombre__icontains=nombre)
        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)
        if proveedor_id:
            qs = qs.filter(proveedor_id=proveedor_id)

        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, producto_id: int):
        try:
            obj = ProductoModel.objects.select_related("proveedor", "categoria").get(id=producto_id)
            return self._to_domain(obj)
        except ProductoModel.DoesNotExist:
            raise RuntimeError(f"Producto no encontrado: {producto_id}")

    def actualizar(self, producto_id: int, producto: Producto):
        try:
            obj = ProductoModel.objects.get(id=producto_id)
        except ProductoModel.DoesNotExist:
            raise RuntimeError(f"Producto no encontrado: {producto_id}")

        proveedor = None
        categoria = None

        if producto.proveedor_id:
            proveedor = ProveedorModel.objects.get(id=producto.proveedor_id)

        if producto.categoria_id:
            categoria = CategoriaModel.objects.get(id=producto.categoria_id)

        obj.fecha = producto.fecha
        obj.nombre = producto.nombre
        obj.descripcion = producto.descripcion
        obj.precio_unitario = producto.precio_unitario
        obj.cantidad = producto.cantidad
        obj.proveedor = proveedor
        obj.categoria = categoria
        obj.activo = producto.activo
        obj.save()

        return self._to_domain(obj)

    def eliminar(self, producto_id: int):
        try:
            obj = ProductoModel.objects.get(id=producto_id)
        except ProductoModel.DoesNotExist:
            raise RuntimeError(f"Producto no encontrado: {producto_id}")

        obj.activo = False
        obj.save()

    def activar(self, producto_id: int):
        try:
            obj = ProductoModel.objects.get(id=producto_id)
        except ProductoModel.DoesNotExist:
            raise RuntimeError(f"Producto no encontrado: {producto_id}")

        obj.activo = True
        obj.save()