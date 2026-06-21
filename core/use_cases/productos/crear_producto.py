from core.domain.entities.producto import Producto


class CrearProductoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        producto = Producto(
            fecha=data["fecha"],
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            precio_unitario=data["precio_unitario"],
            cantidad=data["cantidad"],
            proveedor_id=data.get("proveedor_id"),
            categoria_id=data.get("categoria_id"),
            activo=data.get("activo", True),
        )
        return self.repository.crear(producto)