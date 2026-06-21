import secrets
from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from infrastructure.persistence.repositories.django_password_reset_repository import DjangoPasswordResetRepository


class SolicitarRecuperacionPasswordUseCase:
    def __init__(self, usuario_repository, password_reset_repository, email_service):
        self.usuario_repository = usuario_repository
        self.password_reset_repository = password_reset_repository
        self.email_service = email_service

    def execute(self, correo: str, base_url: str):
        usuario = self.usuario_repository.obtener_por_correo(correo)

        if not usuario or not usuario.activo:
            return False

        token = secrets.token_urlsafe(48)
        self.password_reset_repository.crear(usuario.id, token)

        enlace = f"{base_url}/reset-password/{token}"

        self.email_service.enviar_recuperacion_password(
            destino=usuario.correo,
            nombre=usuario.nombre,
            enlace=enlace,
        )

        return True