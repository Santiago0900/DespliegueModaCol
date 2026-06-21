from core.domain.entities.compra import Compra
from core.domain.entities.detalle_compra import DetalleCompra


class ActualizarCompraUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, compra_id: int, data: dict):
        actual = self.repository.obtener_por_id(compra_id)

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
            id=compra_id,
            numero_compra=actual.numero_compra,
            fecha_compra=data["fecha_compra"],
            fecha_estimada_entrega=data.get("fecha_estimada_entrega"),
            proveedor_id=data["proveedor_id"],
            usuario_id=actual.usuario_id,
            estado=data["estado"],
            observaciones=data.get("observaciones"),
            detalles=detalles,
            activo=data.get("activo", actual.activo),
        )
        return self.repository.actualizar(compra_id, compra)