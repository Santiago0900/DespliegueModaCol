from core.domain.entities.cliente import Cliente


class CrearClienteUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        cliente = Cliente(
            empresa=data["empresa"],
            nombre=data["nombre"],
            identificacion=data["identificacion"],
            contacto=data.get("contacto"),
            correo=data.get("correo"),
            activo=data.get("activo", True),
        )
        return self.repository.crear(cliente)
