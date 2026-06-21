from core.domain.entities.venta import Venta
from core.domain.entities.detalle_venta import DetalleVenta


class CrearVentaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        detalles = [
            DetalleVenta(
                producto_id=d["producto_id"],
                cantidad=d["cantidad"],
                precio_unitario=d["precio_unitario"],
            )
            for d in data.get("detalles", [])
            if d.get("producto_id")
        ]

        if not detalles:
            raise RuntimeError("La venta debe tener al menos un detalle.")

        venta = Venta(
            fecha_venta=data["fecha_venta"],
            cliente_id=data["cliente_id"],
            usuario_id=data["usuario_id"],
            tipo_documento=data["tipo_documento"],
            forma_pago=data["forma_pago"],
            estado=data["estado"],
            observaciones=data.get("observaciones"),
            detalles=detalles,
            activo=data.get("activo", True),
        )
        return self.repository.crear(venta)