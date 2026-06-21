from django.contrib.auth.hashers import make_password


class RestablecerPasswordUseCase:
    def __init__(self, usuario_repository, password_reset_repository):
        self.usuario_repository = usuario_repository
        self.password_reset_repository = password_reset_repository

    def execute(self, token: str, nueva_password: str):
        token_obj = self.password_reset_repository.obtener_token_valido(token)

        if not token_obj:
            return False

        usuario = self.usuario_repository.obtener_por_id(token_obj.usuario.id)
        usuario.password_hash = make_password(nueva_password)

        self.usuario_repository.actualizar(usuario.id, usuario)
        self.password_reset_repository.marcar_como_usado(token_obj)

        return True