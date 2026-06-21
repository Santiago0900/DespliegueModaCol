from core.domain.entities.cliente import Cliente


class ActualizarClienteUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, cliente_id: int, data: dict):
        actual = self.repository.obtener_por_id(cliente_id)

        cliente = Cliente(
            id=cliente_id,
            empresa=data["empresa"],
            nombre=data["nombre"],
            identificacion=data["identificacion"],
            contacto=data.get("contacto"),
            correo=data.get("correo"),
            activo=data.get("activo", actual.activo),
        )
        return self.repository.actualizar(cliente_id, cliente)