from core.domain.entities.usuario import Usuario
from django.contrib.auth.hashers import make_password


class ActualizarUsuarioUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, usuario_id: int, data: dict):
        actual = self.repository.obtener_por_id(usuario_id)

        password_hash = actual.password_hash
        if data.get("password"):
            password_hash = make_password(data["password"])

        usuario = Usuario(
            id=usuario_id,
            nombre=data["nombre"],
            correo=data["correo"],
            password_hash=password_hash,
            rol_id=int(data["rol_id"]),
            activo=data.get("activo", actual.activo),
        )

        return self.repository.actualizar(usuario_id, usuario)