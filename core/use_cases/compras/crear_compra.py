from core.domain.entities.compra import Compra
from core.domain.entities.detalle_compra import DetalleCompra


class CrearCompraUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict, usuario_id: int):
        detalles = [
            DetalleCompra(
                producto_id=d["producto_id"],
                precio_unitario=d["precio_unitario"],
                cantidad=d["cantidad"],
            )
            for d in data.get("detalles", [])
            if d.get("producto_id")
        ]

        compra = Compra(
            fecha_compra=data["fecha_compra"],
            fecha_estimada_entrega=data.get("fecha_estimada_entrega"),
            proveedor_id=data["proveedor_id"],
            usuario_id=usuario_id,
            estado=data.get("estado", "PENDIENTE"),
            observaciones=data.get("observaciones"),
            detalles=detalles,
            activo=data.get("activo", True),
        )
        return self.repository.crear(compra)