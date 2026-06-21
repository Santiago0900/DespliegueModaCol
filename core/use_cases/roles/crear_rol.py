from core.domain.entities.rol import Rol


class CrearRolUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        rol = Rol(
            tipo=data["tipo"].upper(),
            activo=data.get("activo", True),
        )
        return self.repository.crear(rol)