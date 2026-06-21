from django.contrib.auth.hashers import check_password


class LoginUsuarioUseCase:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def execute(self, correo: str, password: str):
        if not correo or not password:
            return {
                "success": False,
                "message": "Debes ingresar correo y contraseña.",
                "usuario": None,
            }

        usuario = self.usuario_repository.obtener_por_correo(correo)

        if not usuario:
            return {
                "success": False,
                "message": "Credenciales inválidas.",
                "usuario": None,
            }

        if not usuario.activo:
            return {
                "success": False,
                "message": "Tu usuario se encuentra inactivo.",
                "usuario": None,
            }

        if not check_password(password, usuario.password_hash):
            return {
                "success": False,
                "message": "Credenciales inválidas.",
                "usuario": None,
            }

        return {
            "success": True,
            "message": "Login exitoso.",
            "usuario": usuario,
        }