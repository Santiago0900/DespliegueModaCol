from core.domain.entities.producto import Producto


class ActualizarProductoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, producto_id: int, data: dict):
        actual = self.repository.obtener_por_id(producto_id)

        producto = Producto(
            id=producto_id,
            fecha=data["fecha"],
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            precio_unitario=data["precio_unitario"],
            cantidad=data["cantidad"],
            proveedor_id=data.get("proveedor_id"),
            categoria_id=data.get("categoria_id"),
            activo=data.get("activo", actual.activo),
        )
        return self.repository.actualizar(producto_id, producto)