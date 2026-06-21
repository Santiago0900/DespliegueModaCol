from core.domain.entities.proveedor import Proveedor


class CrearProveedorUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        proveedor = Proveedor(
            razon_social=data["razon_social"],
            identificacion=data["identificacion"],
            direccion=data.get("direccion"),
            correo=data.get("correo"),
            contacto=data.get("contacto"),
            activo=data.get("activo", True),
        )
        return self.repository.crear(proveedor)