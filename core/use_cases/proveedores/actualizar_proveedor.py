from core.domain.entities.proveedor import Proveedor


class ActualizarProveedorUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, proveedor_id: int, data: dict):
        actual = self.repository.obtener_por_id(proveedor_id)

        proveedor = Proveedor(
            id=proveedor_id,
            razon_social=data["razon_social"],
            identificacion=data["identificacion"],
            direccion=data.get("direccion"),
            correo=data.get("correo"),
            contacto=data.get("contacto"),
            activo=data.get("activo", actual.activo),
        )
        return self.repository.actualizar(proveedor_id, proveedor)