from core.domain.entities.usuario import Usuario
from django.contrib.auth.hashers import make_password


class CrearUsuarioUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        if not data.get("password"):
            raise RuntimeError("La contraseña es obligatoria al crear un usuario")

        if not data.get("rol_id"):
            raise RuntimeError("El rol es obligatorio")

        password_plano = data["password"]

        usuario = Usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            password_hash=make_password(password_plano),
            rol_id=int(data["rol_id"]),
            activo=data.get("activo", True),
        )

        creado = self.repository.crear(usuario)
        creado.password_hash = password_plano  # temporal para usarlo en el correo
        return creado