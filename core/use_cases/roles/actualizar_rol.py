from core.domain.entities.rol import Rol


class ActualizarRolUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, rol_id: int, data: dict):
        actual = self.repository.obtener_por_id(rol_id)
        rol = Rol(
            id=rol_id,
            tipo=data["tipo"].upper(),
            activo=data.get("activo", actual.activo),
        )
        return self.repository.actualizar(rol_id, rol)